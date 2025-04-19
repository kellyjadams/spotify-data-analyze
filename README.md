# spotify-data-analyze

> Currently a work in progress

## Environment

```bash
conda activate spotify-env
```

## Setup

1. **Installation:** Install Spotipy which has access to all endpoints of the Spotify Web API. 
   ```bash
   pip install spotipy
   ```

3. **Setup:**
   - Create an application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
      - App Name
      - App description
      - Redirect URIs: `http://localhost:8080`
      - Which API/SDKs are you planning to use? Check `Web API`
   - Set up a Redirect URI in your application settings; this is required for user authentication.
   - Get Client ID, Client Secret and Redirect URL to put into your file.

4. **Authentication:**
   - Use Spotipy's `SpotifyOAuth` for user authentication.
   - Define the necessary scopes (e.g. `user-top-read`) based on the data you want to see.
   - Add in Client ID, Client Secret and Redirect URL information.

# Deploy

To deploy the latest version:

```bash
./scripts/deploy.sh
```

## File



## Documentation

- Spotipy Documentation: [https://spotipy.readthedocs.io/](https://spotipy.readthedocs.io/)
- Spotify Web API Documentation: [https://developer.spotify.com/documentation/web-api](https://developer.spotify.com/documentation/web-api)
