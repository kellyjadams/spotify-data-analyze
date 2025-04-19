from flask import Flask
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google.cloud import bigquery
from collections import Counter

app = Flask(__name__)

@app.route("/")
def run_pipeline():
    # Load environment variables
    CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
    REFRESH_TOKEN = os.getenv("SPOTIPY_REFRESH_TOKEN")
    GCP_PROJECT = os.getenv("GCP_PROJECT")
    BQ_DATASET = os.getenv("BQ_DATASET")
    BQ_TABLE = os.getenv("BQ_TABLE")
    time_frame = 'long_term'

    # Set up Spotify auth using the refresh token
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-top-read'
    )

    auth_manager.refresh_access_token(REFRESH_TOKEN)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Get top tracks
    top_tracks = sp.current_user_top_tracks(limit=10, time_range=time_frame)
    track_list = [f"{track['name']} by {', '.join(artist['name'] for artist in track['artists'])}" for track in top_tracks['items']]

    # Get top artists
    top_artists = sp.current_user_top_artists(limit=5, time_range=time_frame)
    artist_list = [artist['name'] for artist in top_artists['items']]

    # Calculate total listening time
    all_tracks = sp.current_user_top_tracks(limit=50, time_range=time_frame)
    total_time_ms = sum(track['duration_ms'] for track in all_tracks['items'])
    total_time_minutes = total_time_ms / (1000 * 60)

    # Get top genres
    genres = []
    for artist in top_artists['items']:
        genres.extend(artist['genres'])
    genre_counts = Counter(genres)
    top_genres = [genre for genre, _ in genre_counts.most_common(5)]

    # Prepare row for BigQuery
    row = {
        "time_frame": time_frame,
        "top_tracks": track_list,
        "top_artists": artist_list,
        "top_genres": top_genres,
        "estimated_minutes_listened": round(total_time_minutes, 2)
    }

    # Insert into BigQuery
    client = bigquery.Client(project=GCP_PROJECT)
    table_id = f"{GCP_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"
    errors = client.insert_rows_json(table_id, [row])

    if errors:
        return {"status": "error", "details": errors}, 500
    return {"status": "success", "inserted": row}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
