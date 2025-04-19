# Spotify Listening Logger (Cloud Run + BigQuery)

This project logs my currently playing Spotify track **every minute** using a Python app deployed on **Google Cloud Run**. The data is streamed into **BigQuery**, enabling powerful real-time and historical analysis of your listening habits.

---

## Features

- Polls Spotify every minute to capture now-playing tracks
- Writes rich metadata (track, artist, genre, popularity, etc.) to BigQuery
- Secure credentials via environment variables or GitHub Secrets
- Deployable via Cloud Run and GitHub Actions (CI/CD)
- Ready for Looker Studio dashboards or custom analytics

---

## Project Structure

```
spotify-data-analyze/
├── cloud/
│   └── playback/
│       ├── main.py                # Flask app for Cloud Run
│       ├── Dockerfile             # Container definition
│       ├── requirements.txt       # Python dependencies
│       └── deploy.sh              # Manual deploy script
├── .env                           # Environment variables (Git-ignored)
├── scripts/                       # Optional utility scripts
└── .github/workflows/
    └── cloud-deploy.yml           # GitHub Actions CI/CD workflow
```

---

## Environment Variables

Create a `.env` file in the root with:

```env
SPOTIPY_CLIENT_ID=your-client-id
SPOTIPY_CLIENT_SECRET=your-client-secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
SPOTIPY_REFRESH_TOKEN=your-refresh-token
GCP_PROJECT=your-gcp-project-id
BQ_DATASET=spotify_data
BQ_TABLE=log_tracks
```

> Secrets are injected into Cloud Run using `--set-env-vars`

---

## Deployment (Manual)

```bash
cd cloud/playback
./deploy.sh
```

> This builds a Docker image and deploys it to Cloud Run using the variables from `.env`.

---

## Schedule with Cloud Scheduler

Use Google Cloud Scheduler to trigger your deployed URL every 1 minute:

- Method: `GET`
- Auth: `Unauthenticated`
- URL: `https://your-cloud-run-url/`
- Frequency: `* * * * *`

---

## BigQuery Table Schema

Make sure your table `log_tracks` includes:

| Field         | Type      | Mode     |
|---------------|-----------|----------|
| timestamp     | FLOAT     | NULLABLE |
| track         | STRING    | NULLABLE |
| artists       | STRING    | NULLABLE |
| album         | STRING    | NULLABLE |
| duration_ms   | INTEGER   | NULLABLE |
| genre         | STRING    | NULLABLE |
| popularity    | INTEGER   | NULLABLE |
| explicit      | BOOLEAN   | NULLABLE |

> Use `create-bigquery-table.py` to create the schema (optional).

---

## Analysis

> Work in progress 

---

## Roadmap

- [ ] Create a Cloud Function to compute daily/weekly summaries
- [ ] Stream processed data into a Looker Studio dashboard

---

