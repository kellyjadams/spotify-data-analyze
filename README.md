# Spotify Listening Logger (Cloud Run + BigQuery)

This is a personal data project to demonstrate my **data engineering** and **analytics engineering** skills. It automatically logs my Spotify listening history every minute using a **Python app deployed on Google Cloud Run**, storing the data in **BigQuery** for analysis and dashboarding.

---

## Why I Built This

I wanted to explore how to:

- Build a serverless data pipeline with **Cloud Run**, **Docker**, and **GitHub Actions**
- Manage secrets securely using `.env` and GitHub Secrets
- Orchestrate updates using **Cloud Scheduler**
- Structure data for analysis in **BigQuery**
- Design pipelines that can scale and support real-time insights

This project combines core cloud and analytics engineering tools to build something end-to-end—from ingestion to visualization.

---

## Key Features

- Polls Spotify every minute for now-playing tracks
- Logs detailed track metadata: artist, album, genre, popularity, and more
- Streams data into BigQuery for historical and real-time analysis
- Built with a containerized Python app using Flask
- CI/CD enabled via GitHub Actions
- Ready for Looker Studio dashboards or custom SQL analytics

---

## Technical Skills Demonstrated

- **Python** for API ingestion and transformation
- **Cloud Run + Docker** for serverless deployment
- **GitHub Actions** for CI/CD automation
- **BigQuery** for cloud-native analytics and schema design
- **Cloud Scheduler** for orchestrated polling
- **Environment variable management** for secret handling

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

Create a `.env` file in the root:

```env
SPOTIPY_CLIENT_ID=your-client-id
SPOTIPY_CLIENT_SECRET=your-client-secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
SPOTIPY_REFRESH_TOKEN=your-refresh-token
GCP_PROJECT=your-gcp-project-id
BQ_DATASET=spotify_data
BQ_TABLE=log_tracks
```

> These are injected into Cloud Run during deployment using `--set-env-vars`.

---

## Deployment (Manual)

```bash
cd cloud/playback
./deploy.sh
```

> This builds the Docker image and deploys the app to Cloud Run using your `.env` variables.

---

## Automation with Cloud Scheduler

Use **Google Cloud Scheduler** to trigger the endpoint every minute:

- Method: `GET`
- URL: `https://your-cloud-run-url/`
- Auth: `Unauthenticated`
- Frequency: `* * * * *`

---

## BigQuery Table Schema

The destination table should include:

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

> You can use `create-bigquery-table.py` to create this table.

---

## Roadmap

- [ ] Add Cloud Function to summarize weekly trends
- [ ] Build a Looker Studio dashboard
