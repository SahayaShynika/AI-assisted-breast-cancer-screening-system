"""
Heroku Deployment Configuration
"""
import os

# Create Procfile for Heroku
procfile_content = "web: gunicorn app_production:app"

with open('Procfile', 'w') as f:
    f.write(procfile_content)

# Create runtime.txt for Python version
runtime_content = "python-3.12.0"

with open('runtime.txt', 'w') as f:
    f.write(runtime_content)

print("Heroku deployment files created:")
print("- Procfile: Defines how to run your app")
print("- runtime.txt: Specifies Python version")
print("\nTo deploy to Heroku:")
print("1. Install Heroku CLI")
print("2. Run: heroku create your-app-name")
print("3. Run: git push heroku main")
