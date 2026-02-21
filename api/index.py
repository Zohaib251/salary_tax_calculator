# api/index.py
import sys
import os
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

try:
    # Import your Flask app
    from app import app
    print("✅ Successfully imported app")
except Exception as e:
    print(f"❌ Error importing app: {str(e)}")
    import traceback
    traceback.print_exc()
    raise e

# Vercel serverless function handler
def handler(request, context):
    return app