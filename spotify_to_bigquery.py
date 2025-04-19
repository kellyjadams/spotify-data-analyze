# spotify_to_bigquery.py
from flask import Flask
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google.cloud import bigquery
from collections import Counter

app = Flask(__name__)

@app.route("/")
def run_pipeline():
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
    GCP_PROJECT = os.getenv('GCP_PROJECT')
    BQ_DATASET = os.getenv('BQ_DATASET')
    BQ_TABLE = os.getenv('BQ_TABLE')
    time_frame = 'long_term'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-top-read',
        open_browser=False
    ))

    top_tracks = sp.current_user_top_tracks(limit=10, time_range=time_frame)
    track_list = [f"{track['name']} by {', '.join(artist['name'] for artist in track['artists'])}" for track in top_tracks['items']]

    top_artists = sp.current_user_top_artists(limit=5, time_range=time_frame)
    artist_list = [artist['name'] for artist in top_artists['items']]

    all_tracks = sp.current_user_top_tracks(limit=50, time_range=time_frame)
    total_time_ms = sum(track['duration_ms'] for track in all_tracks['items'])
    total_time_minutes = total_time_ms / (1000 * 60)

    genres = []
    for artist in top_artists['items']:
        genres.extend(artist['genres'])
    genre_counts = Counter(genres)
    top_genres = [genre for genre, _ in genre_counts.most_common(5)]

    row = {
        "time_frame": time_frame,
        "top_tracks": track_list,
        "top_artists": artist_list,
        "top_genres": top_genres,
        "estimated_minutes_listened": round(total_time_minutes, 2)
    }

    client = bigquery.Client(project=GCP_PROJECT)
    table_id = f"{GCP_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"
    errors = client.insert_rows_json(table_id, [row])

    if errors:
        return {"status": "error", "details": errors}, 500
    return {"status": "success", "inserted": row}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
