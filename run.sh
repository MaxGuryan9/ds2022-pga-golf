#!/usr/bin/env bash
docker build -t pga-stats:latest .

docker run --rm -p 8000:8000 pga-stats:latest

curl http://localhost:8000/health
