import os
import cv2
import numpy as np
import tensorflow as tf
from datetime import datetime
from werkzeug.utils import secure_filename

# Simulate the upload and prediction process
def test_upload_simulation():
    print("Testing upload simulation...")
    
    # Load model like the app does
    try:
        model_path = os.path.join(os.getcwd(), 'models', 'densenet121_model.h5')
        print(f"Loading model from: {model_path}")
        model = tf.keras.models.load_model(model_path)
        classes = ["normal", "benign", "malignant"]
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Model loading error: {e}")
        return
    
    # Create a dummy image file
    dummy_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    test_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_test_image.jpg"
    
    # Create upload directory if it doesn't exist
    upload_folder = 'static/uploads'
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save the test image
    filepath = os.path.join(upload_folder, test_filename)
    cv2.imwrite(filepath, dummy_image)
    print(f"Test image saved to: {filepath}")
    print(f"File exists: {os.path.exists(filepath)}")
    
    # Test the prediction function
    try:
        print("\nTesting prediction...")
        
        # Read image
        print(f"Reading image from: {filepath}")
        img = cv2.imread(filepath)
        if img is None:
            print("Failed to read image")
            return
        
        print(f"Image shape before processing: {img.shape}")
        img = cv2.resize(img, (224, 224))
        img = img / 255.0
        img = np.reshape(img, (1, 224, 224, 3))
        print(f"Image shape after processing: {img.shape}")
        
        # Make prediction
        print("Making prediction...")
        prediction = model.predict(img, verbose=0)[0]
        predicted_class = classes[np.argmax(prediction)]
        confidence = float(np.max(prediction))
        
        # Determine cancer stage
        if predicted_class == "normal":
            stage = "No Cancer"
        elif predicted_class == "benign":
            stage = "Early Stage (Benign)"
        else:
            stage = "Advanced Stage (Malignant)"
        
        print(f"Prediction successful!")
        print(f"Result: {predicted_class}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Stage: {stage}")
        
        # Clean up
        os.remove(filepath)
        print(f"\nTest completed successfully! Cleaned up test file.")
        
    except Exception as e:
        print(f"Prediction error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_upload_simulation()
