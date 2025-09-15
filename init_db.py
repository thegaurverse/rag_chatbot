#!/usr/bin/env python3
"""
Database initialization script for Railway deployment.
This script will set up the PGVector extension and initialize the vector database.
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

def setup_pgvector_extension():
    """Set up PGVector extension in PostgreSQL database."""
    load_dotenv()
    
    connection_string = os.getenv("PGVECTOR_CONNECTION_STRING")
    if not connection_string:
        print("❌ PGVECTOR_CONNECTION_STRING not found in environment variables")
        return False
    
    try:
        # Parse connection string to get database details
        print("🔗 Connecting to PostgreSQL database...")
        conn = psycopg2.connect(connection_string)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create PGVector extension
        print("🧩 Creating PGVector extension...")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        # Verify extension is installed
        cursor.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        result = cursor.fetchone()
        
        if result:
            print("✅ PGVector extension installed successfully!")
        else:
            print("❌ Failed to install PGVector extension")
            return False
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error setting up PGVector extension: {str(e)}")
        return False

def initialize_vector_database():
    """Initialize the vector database with health data."""
    try:
        print("📚 Loading and processing health data...")
        
        # Import here to avoid issues if other imports fail
        from text_loader import *
        
        print("✅ Vector database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing vector database: {str(e)}")
        return False

def main():
    """Main initialization function."""
    print("🚀 Starting database initialization for Railway deployment...")
    
    # Step 1: Set up PGVector extension
    if not setup_pgvector_extension():
        print("❌ Failed to set up PGVector extension")
        sys.exit(1)
    
    # Step 2: Initialize vector database
    if not initialize_vector_database():
        print("❌ Failed to initialize vector database")
        sys.exit(1)
    
    print("🎉 Database initialization completed successfully!")

if __name__ == "__main__":
    main()