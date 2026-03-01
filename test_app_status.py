import requests
import time

def test_model_status():
    """Test the model status endpoint"""
    try:
        print("Testing model status endpoint...")
        response = requests.get('http://127.0.0.1:5000/model_status')
        if response.status_code == 200:
            data = response.json()
            print(f"Model status: {data['status']}")
            print(f"Message: {data['message']}")
            return data['status'] == 'loaded'
        else:
            print(f"Error: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Error connecting to app: {e}")
        return False

if __name__ == '__main__':
    # Wait a moment for the app to fully start
    time.sleep(2)
    test_model_status()
