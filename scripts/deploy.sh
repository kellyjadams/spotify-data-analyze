#!/bin/bash

# Load env vars from .env file
source .env

SERVICE_NAME="spotify-pipeline"
REGION="us-central1"
IMAGE="gcr.io/$GCP_PROJECT/$SERVICE_NAME"

# Build Docker image
gcloud builds submit --tag $IMAGE

# Deploy to Cloud Run with all Spotipy + GCP + BigQuery environment variables
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars SPOTIPY_CLIENT_ID=$SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET=$SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI=$SPOTIPY_REDIRECT_URI,SPOTIPY_REFRESH_TOKEN=$SPOTIPY_REFRESH_TOKEN,GCP_PROJECT=$GCP_PROJECT,BQ_DATASET=$BQ_DATASET,BQ_TABLE=$BQ_TABLE
