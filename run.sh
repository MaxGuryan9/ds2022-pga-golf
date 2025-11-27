#!/usr/bin/env bash
set -e

IMAGE_NAME="pga-stats:latest"

# Build the Docker image
docker build -t "$IMAGE_NAME" .

# Run the container, mapping port 8000 → 8000
docker run --rm -p 8000:8000 "$IMAGE_NAME"
