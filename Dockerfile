# Railway-optimized Dockerfile using Python 3.11-slim
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with timeouts and retries
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir --timeout 600 --retries 3 -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway will set PORT env var at runtime)
EXPOSE 8080

# Health check for Railway
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/_stcore/health || exit 1

# Run the application
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true