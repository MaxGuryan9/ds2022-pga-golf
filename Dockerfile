# Use a small, modern Python base image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (helpful for pandas etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source code and templates
COPY src/ /app/src/
COPY templates/ /app/templates/

# Create data directories inside the image
RUN mkdir -p /app/data/raw /app/data/intermediate /app/data/processed

# -------------------------------------------------------------------
# Run the full data pipeline at build time
# This will:
#   - download raw CSVs
#   - parse/clean them
#   - build master_player_seasons.csv
# Each run overwrites existing CSVs because pandas.to_csv defaults to 'w' mode.
# -------------------------------------------------------------------
RUN python src/download_stats.py && \
    python src/parse_stats.py && \
    python src/build_master.py

# Expose the port the Flask app will run on
EXPOSE 8000

# Run the Flask app when the container starts
CMD ["python", "src/app.py"]
