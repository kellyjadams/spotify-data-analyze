# Load environment variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../.env"

SERVICE_NAME="spotify-playback-tracker"
REGION="us-central1"
IMAGE="gcr.io/$GCP_PROJECT/$SERVICE_NAME"
SERVICE_ACCOUNT="spotify-to-bigquery@$GCP_PROJECT.iam.gserviceaccount.com"

# Build Docker image
gcloud builds submit cloud/playback --tag $IMAGE

# Deploy to Cloud Run (secure, no key file, with service account)
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --platform managed \
  --region $REGION \
  --service-account $SERVICE_ACCOUNT \
  --no-allow-unauthenticated \
  --set-env-vars SPOTIPY_CLIENT_ID=$SPOTIPY_CLIENT_ID,\
SPOTIPY_CLIENT_SECRET=$SPOTIPY_CLIENT_SECRET,\
SPOTIPY_REDIRECT_URI=$SPOTIPY_REDIRECT_URI,\
SPOTIPY_REFRESH_TOKEN=$SPOTIPY_REFRESH_TOKEN,\
GCP_PROJECT=$GCP_PROJECT,\
BQ_DATASET=$BQ_DATASET,\
BQ_TABLE=$BQ_TABLE
