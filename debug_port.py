#!/usr/bin/env python3
"""
Debug script to check environment variables in Railway
"""
import os

print("🔍 Environment Variable Debug:")
print(f"PORT: {os.environ.get('PORT', 'NOT SET')}")
print(f"STREAMLIT_SERVER_PORT: {os.environ.get('STREAMLIT_SERVER_PORT', 'NOT SET')}")

# Print all environment variables that contain 'PORT'
print("\n📋 All PORT-related environment variables:")
for key, value in os.environ.items():
    if 'PORT' in key.upper():
        print(f"{key}: {value}")

print(f"\n✅ Using port: {os.environ.get('PORT', '8080')}")