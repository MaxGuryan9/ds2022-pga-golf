# Use a small, modern Python base image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (optional, but good for pandas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Create expected directories
RUN mkdir -p /app/data/raw /app/data/intermediate /app/data/processed
RUN mkdir -p /app/src /app/templates

# Copy source code and templates
COPY src/ /app/src/
COPY templates/ /app/templates/

# Copy processed data (pre-built on your machine)
# This should include master_player_seasons.csv
COPY data/processed/ /app/data/processed/

# Expose the port the Flask app will run on
EXPOSE 8000

# Default command: run the Flask app
CMD ["python", "src/app.py"]
