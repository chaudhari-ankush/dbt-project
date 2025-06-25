# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/dbt_project

# Copy the application code
COPY app/ ./app/
COPY dbt_project.yml /app/dbt_project/
COPY profiles.yml /app/dbt_project/
COPY . /app

# Set environment variables
ENV PYTHONPATH=/app \
    DBT_PROFILES_DIR=/app/dbt_project \
    PYTHONUNBUFFERED=1 \
    AWS_DEFAULT_REGION=us-east-2

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Verify files
RUN ls -l /app 