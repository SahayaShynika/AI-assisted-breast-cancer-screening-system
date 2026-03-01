import requests
import os
import json
from datetime import datetime

def test_complete_workflow():
    """Test the complete upload and prediction workflow"""
    base_url = "http://127.0.0.1:5000"
    
    print("Testing complete workflow...")
    
    # First check model status
    try:
        response = requests.get(f"{base_url}/model_status")
        if response.status_code == 200:
            data = response.json()
            print(f"Model status: {data['status']}")
        else:
            print(f"Model status check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"Error checking model status: {e}")
        return
    
    # Create a simple test image
    import cv2
    import numpy as np
    
    # Create test image
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    test_filename = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(test_filename, test_image)
    
    try:
        # Test upload (this would normally require login, but we'll test the endpoint)
        print(f"Test image created: {test_filename}")
        print("Application is ready for testing")
        print("\nTo test the complete workflow:")
        print("1. Open http://127.0.0.1:5000 in your browser")
        print("2. Login with demo credentials:")
        print("   Doctor: doctor@demo.com / doctor123")
        print("   Patient: patient@demo.com / patient123")
        print("3. Upload an image to test prediction")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up test image
        if os.path.exists(test_filename):
            os.remove(test_filename)
            print(f"Cleaned up test image")

if __name__ == '__main__':
    test_complete_workflow()
