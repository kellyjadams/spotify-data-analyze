import os
import spotipy
from collections import Counter
from spotipy.oauth2 import SpotifyOAuth

import os

# Load credentials from a text file
def load_credentials(file_path):
    credentials = {}
    with open(file_path, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            credentials[key] = value
    return credentials

# Load credentials
creds = load_credentials('spotify_credentials.txt')

# Set secret info
CLIENT_ID = creds['CLIENT_ID']
CLIENT_SECRET = creds['CLIENT_SECRET']
REDIRECT_URI = creds['REDIRECT_URI']

# Set time frame
time_frame = 'long_term'

# Define the scope
scope = 'user-top-read'

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope
))

# Top 10 Songs
results = sp.current_user_top_tracks(limit=10, time_range=time_frame)  # Options: short_term, medium_term, long_term

# Display results
print("Your Top 10 Songs:")
for idx, track in enumerate(results['items']):
    print(f"{idx + 1}: {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")

# Top 5 Artists
top_artists = sp.current_user_top_artists(limit=5, time_range=time_frame)
print("\nYour Top 5 Artists:")
for idx, artist in enumerate(top_artists['items']):
    print(f"{idx + 1}: {artist['name']}")

# Total Listening Time (Top Tracks)
top_tracks = sp.current_user_top_tracks(limit=50, time_range=time_frame)
total_time_ms = sum(track['duration_ms'] for track in top_tracks['items'])
total_time_minutes = total_time_ms / (1000 * 60)
print(f"\nEstimated Total Listening Time for Top Tracks: {total_time_minutes:.2f} minutes")

# Top Genres
genres = []
for artist in top_artists['items']:
    genres.extend(artist['genres'])
genre_counts = Counter(genres)
print("\nYour Top Genres:")
for genre, count in genre_counts.most_common(5):
    print(f"{genre}: {count} artists")
