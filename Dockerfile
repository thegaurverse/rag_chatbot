# Simplified single-stage build for Railway
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libopenblas-dev \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements
COPY requirements.txt .

# Install Python dependencies step by step
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --timeout 600 --retries 3 -r requirements.txt

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x start.sh
RUN chmod +x run_app.py

# Expose default port (Railway will set PORT env var at runtime)
EXPOSE 8080

# Run the application using startup script
CMD ["sh", "-c", "./start.sh"]
