#!/usr/bin/env python3
"""
Python launcher for Railway Streamlit deployment
Handles PORT environment variable configuration reliably
"""
import os
import sys
import subprocess

def main():
    # Clear any conflicting Streamlit environment variables
    if 'STREAMLIT_SERVER_PORT' in os.environ:
        del os.environ['STREAMLIT_SERVER_PORT']
    
    # Get port from environment with fallback
    port = os.environ.get('PORT', '8080')
    
    print(f"🚀 Starting Streamlit on port {port}...")
    print(f"📍 Current working directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    
    # Verify Streamlit is available
    try:
        import streamlit
        print(f"📊 Streamlit version: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit not found!")
        sys.exit(1)
    
    # Build the command
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        '--server.port', str(port),
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.runOnSave', 'false',
        '--server.allowRunOnSave', 'false'
    ]
    
    print(f"🔧 Running command: {' '.join(cmd)}")
    
    # Execute Streamlit
    try:
        os.execvp(sys.executable, cmd)
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()