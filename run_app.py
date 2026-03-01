import os
import sys

def main():
    print("Starting Breast Cancer Detection App...")
    print("=" * 50)
    
    # Check if model exists
    model_path = 'models/densenet121_model.h5'
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return
    
    print(f"Model found: {model_path}")
    print("Starting Flask application...")
    print("The app will be available at: http://127.0.0.1:5000")
    print("\nDemo credentials:")
    print("Doctor: doctor@demo.com / doctor123")
    print("Patient: patient@demo.com / patient123")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the app
    from app_fixed import app
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    main()
