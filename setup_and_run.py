#!/usr/bin/env python3
"""
Breast Cancer Detection System - Simple Setup and Run
"""

import os
import sys
import subprocess

def print_banner():
    print("=" * 60)
    print("    BREAST CANCER DETECTION SYSTEM")
    print("    Powered by DenseNet-121 AI Technology")
    print("=" * 60)
    print()

def check_requirements():
    print("Checking requirements...")
    
    try:
        import tensorflow as tf
        print(f"TensorFlow {tf.__version__} - OK")
    except ImportError:
        print("ERROR: TensorFlow not installed")
        return False
    
    try:
        import flask
        print(f"Flask {flask.__version__} - OK")
    except ImportError:
        print("ERROR: Flask not installed")
        return False
    
    print("All requirements satisfied!\n")
    return True

def check_dataset():
    print("Checking dataset...")
    
    if not os.path.exists("dataset/train"):
        print("ERROR: Training dataset not found")
        return False
    
    if not os.path.exists("dataset/test"):
        print("ERROR: Testing dataset not found")
        return False
    
    print("Dataset found - OK\n")
    return True

def train_model():
    print("Training model...")
    
    if not check_dataset():
        print("Cannot train without dataset")
        return False
    
    try:
        print("Starting training process...")
        result = subprocess.run([sys.executable, "enhanced_train.py"], 
                              capture_output=True, text=True, timeout=3600)
        
        if result.returncode == 0:
            print("Model training completed successfully!")
            return True
        else:
            print("Model training failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Training error: {e}")
        return False

def run_application():
    print("Starting web application...")
    print("Open http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nApplication stopped by user")

def main():
    print_banner()
    
    while True:
        print("What would you like to do?")
        print("1. Check requirements")
        print("2. Train the AI model")
        print("3. Run the web application")
        print("4. Full setup and run")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\n" + "="*40)
            check_requirements()
            check_dataset()
            print("="*40 + "\n")
            
        elif choice == '2':
            print("\n" + "="*40)
            train_model()
            print("="*40 + "\n")
            
        elif choice == '3':
            print("\n" + "="*40)
            run_application()
            print("="*40 + "\n")
            
        elif choice == '4':
            print("\n" + "="*40)
            print("Running complete setup...")
            
            if not check_requirements():
                print("Please install requirements first:")
                print("pip install -r requirements.txt")
                continue
                
            if not check_dataset():
                print("Please setup dataset first")
                continue
                
            if not os.path.exists("models/densenet121_model.h5"):
                print("Training model...")
                if not train_model():
                    print("Training failed!")
                    continue
            
            print("Starting application...")
            run_application()
            print("="*40 + "\n")
            
        elif choice == '5':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
