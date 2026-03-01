import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Import the production Flask app
from app_production import app

# Vercel serverless function handler
def handler(request):
    """
    Vercel serverless function handler
    """
    return app(request.environ, lambda status, headers: None)

# Export for Vercel
app_handler = handler

# For local testing
if __name__ == "__main__":
    app.run(debug=False, port=5000)
