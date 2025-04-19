#!/bin/bash

source .env

SERVICE_NAME="spotify-pipeline"
REGION="us-central1"
IMAGE="gcr.io/$GCP_PROJECT/$SERVICE_NAME"

gcloud builds submit --tag $IMAGE

gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID,SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET,SPOTIFY_REDIRECT_URI=$SPOTIFY_REDIRECT_URI,GCP_PROJECT=$GCP_PROJECT,BQ_DATASET=$BQ_DATASET,BQ_TABLE=$BQ_TABLE
