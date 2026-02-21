# api/index.py
import sys
import os
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

# Import your Flask app
from app import app

# Vercel serverless function handler
def handler(request, context):
    return app