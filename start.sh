#!/bin/bash
# Railway startup script for Streamlit
# Handles PORT environment variable properly

# Clear any conflicting Streamlit environment variables
unset STREAMLIT_SERVER_PORT

# Set port with fallback
if [ -z "$PORT" ]; then
    export PORT=8080
fi

echo "Starting Streamlit on port $PORT..."
echo "Current working directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Streamlit version: $(streamlit --version)"

# Start Streamlit with explicit port
exec streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.runOnSave=false \
    --server.allowRunOnSave=false