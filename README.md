# Spotify Listening Logger (Cloud Run + BigQuery)


This is a personal data project focusing on **data engineering** and **analytics engineering** skills.

- **Data engineering**: ETL pipelines, orchestration, and cloud infrastructure  
- **Analytics engineering**: **BigQuery SQL**, data modeling, building analysis-ready datasets

It automatically logs my Spotify listening history every minute and stores it in **BigQuery** for analysis.

---

## Why I Built This

At the end of the year, I want to compare what's logged in BigQuery with my annual **Spotify Wrapped**.

I wanted to explore how to:

- Build a serverless data pipeline using **Cloud Run**, **Docker**, and **GitHub Actions**
- Manage secrets securely with `.env` files and **GitHub Secrets**
- Schedule and orchestrate updates using **Cloud Scheduler**
- Structure and transform data for analysis in **BigQuery**
- Design pipelines that are scalable and support near real-time insights

This project brings together core **cloud** and **analytics engineering** tools to build something end-to-end—from ingestion to analysis.

---

## Key Features

You’re spot on — your current README is already clear and structured, but now that **"Data Lifecycle"** explains the process well, the **Key Features** section feels slightly redundant.

Instead of repeating what’s already covered later, you can reframe **Key Features** into a quick overview with subsections to match the lifecycle. This keeps it **concise** and **aligned** with your pipeline.

Here’s a refactored version 👇

---

## Key Features

### Data Ingestion & Deployment
- Polls Spotify’s now-playing endpoint every minute using a serverless Cloud Run app
- Built with a containerized Python app using Flask + Spotipy
- Deployed manually using a shell script; Cloud Scheduler handles orchestration by triggering the Cloud Run endpoint every minute.

### Data Storage & Modeling
- Streams listening history into **BigQuery**
- Cleans and deduplicates plays for session-level analysis
- Stores detailed metadata: artist, album, genre, popularity, duration

### Analysis & Visualization
- Designed analysis-ready datasets using **BigQuery SQL**
- Built a [**Looker Studio dashboard**](https://lookerstudio.google.com/reporting/e2f6d5f3-c3cf-4687-ba01-d3a47a15998c) for:
  - Listening trends (songs, minutes, heatmap)
  - Top artists and genres
  - Average song length

---

## Technical Skills

- **Data Pipeline Design**: Built a serverless ETL pipeline from Spotify API to BigQuery using Python and Cloud Run
- **Cloud-Native ETL**: Extracted, transformed, and loaded data on a schedule using Cloud Scheduler and containerized Flask app
- **Python**: Wrote ingestion and transformation logic using the `Spotipy` library
- **REST API**: Created a lightweight endpoint to trigger ingestion using Flask
- **BigQuery**: Designed table schema and streamed structured data for analysis
- **Docker + Cloud Run**: Packaged and deployed the app as a scalable container
- **CI/CD**: Automated deployment via GitHub Actions for reproducibility and version control (*work in progress*)
- **Environment variable management**: Handled secrets securely using `.env` and GitHub Secrets

---

## Project Structure

```
spotify-data-analyze/
spotify-data-analyze/
├── analysis/
│   ├── queries/
│   │   ├── all_artists.sql
│   │   ├── all_genres.sql
│   │   └── heatmap_songs.sql
│   │   └── listening_over_time.sql
│   │   └── songs_played_over_time.sql
│   │   └── top_kpis.sql
│   ├── views/
│   │   ├── deduped_plays_pacific.sql
├── cloud/
│   └── playback/
│       ├── main.py
│       ├── Dockerfile
│       ├── requirements.txt
│       └── deploy.sh
├── scripts/
│   ├── create_bigquery_table.py            
│   ├── delete_bigquery_table.py            
│   └── load_env.py                
├── .env                           
└── .github/workflows/
    └── cloud-deploy.yml
```

---


## Environment & Deployment

This project uses a `.env` file for Spotify and GCP credentials. These variables are injected during Cloud Run deployment.

I deployed the app manually using:

```bash
cd cloud/playback
./deploy.sh
```

I automated ingestion, by setting up a **Cloud Scheduler** job to hit the app endpoint every minute.

The data is stored in a **BigQuery** table with fields like `track`, `artist`, `genre`, and `popularity`. See `create_bigquery_table.py` for schema setup.

> Full setup instructions and configuration details are available in the [blog post](#).

