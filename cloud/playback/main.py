from flask import Flask
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google.cloud import bigquery
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()  # Load from .env in the same directory

@app.route("/")
def log_currently_playing():
    # Load from environment
    CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
    REFRESH_TOKEN = os.getenv("SPOTIPY_REFRESH_TOKEN")
    GCP_PROJECT = os.getenv("GCP_PROJECT")
    BQ_DATASET = os.getenv("BQ_DATASET")
    BQ_TABLE = os.getenv("BQ_TABLE")

    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-read-currently-playing'
    )

    auth_manager.refresh_access_token(REFRESH_TOKEN)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Get current playback
    track = sp.currently_playing()

    if track and track.get("is_playing"):
        artist_ids = [artist["id"] for artist in track["item"]["artists"]]
        genres = set()
        for artist_id in artist_ids:
            artist_info = sp.artist(artist_id)
            genres.update(artist_info.get("genres", []))

        log = {
            "timestamp": time.time(),
            "track": track["item"]["name"],
            "artists": ", ".join([artist["name"] for artist in track["item"]["artists"]]),
            "album": track["item"]["album"]["name"],
            "duration_ms": track["item"]["duration_ms"],
            "genre": ", ".join(genres),
            "popularity": track["item"]["popularity"],
            "explicit": track["item"]["explicit"]
        }

        client = bigquery.Client()
        table_ref = client.dataset(BQ_DATASET).table(BQ_TABLE)
        errors = client.insert_rows_json(table_ref, [log])

        if errors:
            return {"status": "error", "details": errors}, 500
        return {"status": "success", "log": log}, 200

    return {"status": "nothing_playing"}, 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
