#!/bin/sh
# Startup script for Railway deployment
# Uses PORT environment variable or defaults to 8080

port=${PORT:-8080}
echo "Starting Streamlit on port $port..."
echo "Current working directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Streamlit version: $(streamlit --version)"

# Start Streamlit with Railway-optimized settings
exec streamlit run app_simple.py \
    --server.port=$port \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.runOnSave=false \
    --server.allowRunOnSave=false