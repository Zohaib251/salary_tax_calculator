# api/index.py
import sys
import os
import traceback
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

print("="*50)
print("Starting api/index.py")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")
print("="*50)

try:
    # Import your Flask app
    from app import app
    print("✅ Successfully imported app")
except Exception as e:
    print("❌ Error importing app:")
    print(str(e))
    print(traceback.format_exc())
    raise e

# Vercel serverless function handler
def handler(request, context):
    print("✅ Handler called")
    return app