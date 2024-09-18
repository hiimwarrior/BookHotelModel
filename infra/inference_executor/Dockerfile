# Use the official Python 3.11 slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy necessary files
COPY requirements.txt .
COPY inference.py .
COPY entrypoint.sh .
COPY config.py .
COPY .env .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure entrypoint.sh has execution permissions
RUN chmod +x entrypoint.sh

# Define the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
