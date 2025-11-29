#!/usr/bin/env bash
set -e

echo "Running smoke tests..."
pytest tests/test_app.py tests/test_data.py

echo "Tests passed. Building Docker image..."
docker build -t pga-stats:latest .

docker run --rm -p 8000:8000 pga-stats:latest
