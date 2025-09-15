#!/usr/bin/env python3
"""
Railway-compatible Streamlit launcher
This Python script handles port configuration more reliably than shell scripts
"""
import os
import sys
import subprocess

def main():
    # Get port from environment with fallback
    port = os.environ.get('PORT', '8080')
    
    # Clear any conflicting Streamlit environment variables
    if 'STREAMLIT_SERVER_PORT' in os.environ:
        del os.environ['STREAMLIT_SERVER_PORT']
    
    print(f"Starting Streamlit on port {port}...")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Build streamlit command
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'app_simple.py',
        '--server.port', str(port),
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.runOnSave', 'false',
        '--server.allowRunOnSave', 'false'
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Execute streamlit
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()