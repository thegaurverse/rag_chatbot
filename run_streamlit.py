import os
import subprocess
import sys

# Get port from Railway environment
port = os.environ.get('PORT', '8080')
print(f"Starting Streamlit on port {port}")

# Run streamlit with proper Railway settings
cmd = [
    'streamlit', 'run', 'app.py',
    '--server.port', port,
    '--server.address', '0.0.0.0',
    '--server.headless', 'true',
    '--server.fileWatcherType', 'none',
    '--server.runOnSave', 'false'
]

print(f"Executing: {' '.join(cmd)}")
try:
    subprocess.run(cmd, check=True)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)