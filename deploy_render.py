"""
Render.com Deployment Configuration
"""
import yaml

# Create render.yaml for Render.com
render_config = {
    'services': [{
        'type': 'web',
        'name': 'breast-cancer-screening',
        'env': 'python',
        'plan': 'free',
        'buildCommand': 'pip install -r requirements.txt',
        'startCommand': 'gunicorn app_production:app',
        'envVars': [
            {'key': 'PYTHON_VERSION', 'value': '3.12'}
        ]
    }]
}

with open('render.yaml', 'w') as f:
    yaml.dump(render_config, f, default_flow_style=False)

print("Render.com deployment configuration created!")
print("\nTo deploy to Render.com:")
print("1. Go to render.com")
print("2. Connect your GitHub repository")
print("3. Render will automatically detect and deploy your app")
