import tensorflow as tf
import numpy as np
import cv2
import os
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BreastCancerPredictor:
    def __init__(self, model_path='models/densenet121_model.h5'):
        """
        Initialize the breast cancer predictor
        """
        self.model_path = model_path
        self.classes = ['normal', 'benign', 'malignant']
        self.img_size = (224, 224)
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                logger.info(f"Model loaded successfully from {self.model_path}")
            else:
                logger.error(f"Model not found at {self.model_path}")
                raise FileNotFoundError(f"Model not found at {self.model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def preprocess_image(self, image_path):
        """
        Preprocess the image for prediction
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image from {image_path}")
            
            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Resize image
            img = cv2.resize(img, self.img_size)
            
            # Normalize pixel values
            img = img / 255.0
            
            # Add batch dimension
            img = np.reshape(img, (1, self.img_size[0], self.img_size[1], 3))
            
            return img
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    def predict_single_image(self, image_path):
        """
        Make prediction on a single image
        """
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            
            # Make prediction
            predictions = self.model.predict(processed_img, verbose=0)
            
            # Get predicted class and confidence
            predicted_class_idx = np.argmax(predictions[0])
            predicted_class = self.classes[predicted_class_idx]
            confidence = float(np.max(predictions[0]))
            
            # Get all class probabilities
            class_probabilities = {
                self.classes[i]: float(predictions[0][i]) 
                for i in range(len(self.classes))
            }
            
            # Determine cancer stage
            cancer_stage = self.determine_cancer_stage(predicted_class, confidence)
            
            # Create result dictionary
            result = {
                'predicted_class': predicted_class,
                'confidence': confidence,
                'cancer_stage': cancer_stage,
                'class_probabilities': class_probabilities,
                'timestamp': datetime.now().isoformat(),
                'image_path': image_path
            }
            
            logger.info(f"Prediction completed: {predicted_class} with {confidence:.2f} confidence")
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise
    
    def determine_cancer_stage(self, predicted_class, confidence):
        """
        Determine cancer stage based on prediction
        """
        if predicted_class == "normal":
            return "No Cancer Detected"
        elif predicted_class == "benign":
            if confidence > 0.8:
                return "Early Stage (Benign)"
            else:
                return "Possible Benign - Further Evaluation Needed"
        else:  # malignant
            if confidence > 0.8:
                return "Advanced Stage (Malignant) - Immediate Attention Required"
            elif confidence > 0.6:
                return "Likely Malignant - Urgent Consultation Recommended"
            else:
                return "Possible Malignant - Immediate Medical Evaluation Required"
    
    def batch_predict(self, image_paths):
        """
        Make predictions on multiple images
        """
        results = []
        for image_path in image_paths:
            try:
                result = self.predict_single_image(image_path)
                results.append(result)
            except Exception as e:
                logger.error(f"Error predicting {image_path}: {str(e)}")
                results.append({
                    'image_path': image_path,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        return results
    
    def get_model_info(self):
        """
        Get information about the loaded model
        """
        if self.model is None:
            return None
        
        return {
            'model_path': self.model_path,
            'input_shape': self.model.input_shape,
            'output_shape': self.model.output_shape,
            'classes': self.classes,
            'total_params': self.model.count_params(),
            'load_time': datetime.now().isoformat()
        }
    
    def validate_image(self, image_path):
        """
        Validate if the image is suitable for prediction
        """
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                return False, "File does not exist"
            
            # Check file size (max 16MB)
            file_size = os.path.getsize(image_path)
            if file_size > 16 * 1024 * 1024:
                return False, "File size too large (max 16MB)"
            
            # Try to read the image
            img = cv2.imread(image_path)
            if img is None:
                return False, "Invalid image format"
            
            # Check image dimensions
            if img.shape[0] < 100 or img.shape[1] < 100:
                return False, "Image too small (minimum 100x100 pixels)"
            
            return True, "Image is valid"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"

# Global predictor instance
predictor = None

def get_predictor():
    """Get or create the global predictor instance"""
    global predictor
    if predictor is None:
        predictor = BreastCancerPredictor()
    return predictor

def predict_image(image_path):
    """
    Convenience function for single image prediction
    """
    pred = get_predictor()
    return pred.predict_single_image(image_path)

# Test function
def test_prediction():
    """
    Test the prediction system
    """
    try:
        pred = get_predictor()
        
        # Print model info
        model_info = pred.get_model_info()
        print("Model Information:")
        for key, value in model_info.items():
            print(f"  {key}: {value}")
        
        # Test with a sample image if available
        test_image = "dataset/test/normal/normal_001.jpg"  # Adjust path as needed
        if os.path.exists(test_image):
            print(f"\nTesting with image: {test_image}")
            result = pred.predict_single_image(test_image)
            print("Prediction Result:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print(f"\nTest image not found at {test_image}")
            
    except Exception as e:
        print(f"Test failed: {str(e)}")

if __name__ == "__main__":
    test_prediction()
