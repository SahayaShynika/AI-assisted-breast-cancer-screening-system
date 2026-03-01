import tensorflow as tf
import os
import numpy as np

print("Testing model loading...")
print(f"Model file exists: {os.path.exists('models/densenet121_model.h5')}")

if os.path.exists('models/densenet121_model.h5'):
    try:
        print("Attempting to load model...")
        model = tf.keras.models.load_model('models/densenet121_model.h5')
        print("Model loaded successfully!")
        print(f"Model input shape: {model.input_shape}")
        print(f"Model output shape: {model.output_shape}")
        
        # Test prediction with dummy data
        dummy_input = np.random.random((1, 224, 224, 3))
        prediction = model.predict(dummy_input, verbose=0)
        print(f"Test prediction successful: {prediction.shape}")
        print("Model is working correctly!")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        print(f"Error type: {type(e).__name__}")
else:
    print("Model file not found!")
