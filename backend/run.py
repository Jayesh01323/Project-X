#!/usr/bin/env python3
"""
Run script for Project-X FastAPI Backend
This script sets up the Python path and starts the uvicorn server.
"""

import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Now import and run uvicorn
if __name__ == "__main__":
    import uvicorn
    
    print(f"Starting {sys.path[0]}")
    print("Python path configured successfully")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )