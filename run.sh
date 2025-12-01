#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8000}"

echo "Ensuring port ${PORT} is free..."
if lsof -tiTCP:"${PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Port ${PORT} in use. Attempting to terminate listener(s)..."
  pids=$(lsof -tiTCP:"${PORT}" -sTCP:LISTEN)
  kill ${pids}
  sleep 1
fi

if lsof -tiTCP:"${PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Port ${PORT} is still in use. Please free it manually and rerun." >&2
  exit 1
fi

echo "Building image..."
docker build -t pga-stats:latest .

echo "Starting container on port ${PORT}..."
docker run --rm -p "${PORT}:8000" pga-stats:latest

echo "Health check..."
curl "http://localhost:${PORT}/health"
