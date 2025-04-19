# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir spotipy google-cloud-bigquery flask

# Expose HTTP port
EXPOSE 8080

# Run Flask app
CMD ["python", "spotify_to_bigquery.py"]
