#!/bin/bash
# Startup script for Railway deployment
# Uses PORT environment variable or defaults to 8080

PORT=${PORT:-8080}
echo "Starting Streamlit on port $PORT"

exec streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.runOnSave=false \
    --server.allowRunOnSave=false