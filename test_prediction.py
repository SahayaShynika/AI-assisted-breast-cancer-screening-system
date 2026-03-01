import tensorflow as tf
import numpy as np
import cv2
import os

print("Testing model prediction functionality...")

# Load model
try:
    model = tf.keras.models.load_model('models/densenet121_model.h5')
    classes = ["normal", "benign", "malignant"]
    print("Model loaded successfully!")
    print(f"Model input shape: {model.input_shape}")
    print(f"Model output shape: {model.output_shape}")
    
    # Test with random data
    print("\nTesting with random data...")
    dummy_input = np.random.random((1, 224, 224, 3))
    prediction = model.predict(dummy_input, verbose=0)
    predicted_class = classes[np.argmax(prediction)]
    confidence = float(np.max(prediction))
    print(f"Random data prediction: {predicted_class} (confidence: {confidence:.2f})")
    
    # Test with actual image processing pipeline
    print("\nTesting image processing pipeline...")
    
    # Create a dummy image file
    dummy_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    cv2.imwrite('test_image.jpg', dummy_image)
    
    # Process image as the app would
    img = cv2.imread('test_image.jpg')
    if img is None:
        print("Error: Could not read test image")
    else:
        img = cv2.resize(img, (224, 224))
        img = img / 255.0
        img = np.reshape(img, (1, 224, 224, 3))
        
        prediction = model.predict(img, verbose=0)[0]
        predicted_class = classes[np.argmax(prediction)]
        confidence = float(np.max(prediction))
        
        print(f"Image prediction: {predicted_class} (confidence: {confidence:.2f})")
        
        # Determine cancer stage
        if predicted_class == "normal":
            stage = "No Cancer"
        elif predicted_class == "benign":
            stage = "Early Stage (Benign)"
        else:
            stage = "Advanced Stage (Malignant)"
        
        print(f"Cancer stage: {stage}")
    
    # Clean up
    if os.path.exists('test_image.jpg'):
        os.remove('test_image.jpg')
    
    print("\nAll tests completed successfully!")
    
except Exception as e:
    print(f"Error during testing: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
