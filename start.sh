#!/bin/sh
# Startup script for Railway deployment
# Uses PORT environment variable or defaults to 8080

# Clear any conflicting Streamlit environment variables
unset STREAMLIT_SERVER_PORT

# Set port with fallback
PORT=${PORT:-8080}

echo "Starting Streamlit on port $PORT..."
echo "Current working directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Streamlit version: $(streamlit --version)"
echo "PORT environment variable: $PORT"

# Start Streamlit with explicit port using ${PORT} syntax
exec python -m streamlit run app_simple.py \
    --server.port=${PORT} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.runOnSave=false \
    --server.allowRunOnSave=false
