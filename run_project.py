#!/usr/bin/env python3
"""
Breast Cancer Detection System - Project Runner
This script helps set up and run the complete project
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def print_banner():
    """Print project banner"""
    print("=" * 60)
    print("    BREAST CANCER DETECTION SYSTEM")
    print("    Powered by DenseNet-121 AI Technology")
    print("=" * 60)
    print()

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__}")
    except ImportError:
        print("❌ TensorFlow not installed")
        return False
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__}")
    except ImportError:
        print("❌ Flask not installed")
        return False
    
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV not installed")
        return False
    
    try:
        import mysql.connector
        print("✅ MySQL Connector")
    except ImportError:
        print("❌ MySQL Connector not installed")
        return False
    
    print("✅ All requirements satisfied!\n")
    return True

def check_dataset():
    """Check if dataset exists"""
    print("📁 Checking dataset...")
    
    train_path = "dataset/train"
    test_path = "dataset/test"
    
    if not os.path.exists(train_path):
        print("❌ Training dataset not found")
        return False
    
    if not os.path.exists(test_path):
        print("❌ Testing dataset not found")
        return False
    
    # Check for class directories
    classes = ['normal', 'benign', 'malignant']
    for cls in classes:
        if not os.path.exists(os.path.join(train_path, cls)):
            print(f"❌ Training class '{cls}' not found")
            return False
        if not os.path.exists(os.path.join(test_path, cls)):
            print(f"❌ Testing class '{cls}' not found")
            return False
    
    # Count images
    total_train = 0
    total_test = 0
    
    for cls in classes:
        train_count = len([f for f in os.listdir(os.path.join(train_path, cls)) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        test_count = len([f for f in os.listdir(os.path.join(test_path, cls)) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        total_train += train_count
        total_test += test_count
        print(f"   {cls}: {train_count} train, {test_count} test")
    
    print(f"✅ Dataset found: {total_train} training, {total_test} testing images\n")
    return True

def check_model():
    """Check if trained model exists"""
    print("🤖 Checking model...")
    
    model_path = "models/densenet121_model.h5"
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"✅ Model found: {model_path} ({size_mb:.1f} MB)\n")
        return True
    else:
        print("❌ Model not found - training required\n")
        return False

def setup_database():
    """Setup MySQL database"""
    print("🗄️  Setting up database...")
    
    db_setup_file = "database_setup.sql"
    if not os.path.exists(db_setup_file):
        print("❌ Database setup file not found")
        return False
    
    try:
        # Try to connect and run setup
        import mysql.connector
        
        # Note: User should update connection details
        print("⚠️  Please ensure MySQL is running and update connection details")
        print("   Then run: mysql -u root -p < database_setup.sql")
        print("✅ Database setup file ready\n")
        return True
        
    except ImportError:
        print("❌ MySQL connector not installed")
        return False

def train_model():
    """Train the model"""
    print("🎯 Training model...")
    
    if not check_dataset():
        print("❌ Cannot train without dataset")
        return False
    
    try:
        print("   Starting training process...")
        result = subprocess.run([sys.executable, "enhanced_train.py"], 
                              capture_output=True, text=True, timeout=3600)
        
        if result.returncode == 0:
            print("✅ Model training completed successfully!")
            print(result.stdout)
            return True
        else:
            print("❌ Model training failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Training timed out (took too long)")
        return False
    except Exception as e:
        print(f"❌ Training error: {e}")
        return False

def run_application():
    """Run the Flask application"""
    print("🚀 Starting web application...")
    
    try:
        print("   Starting Flask server...")
        print("   📱 Open http://localhost:5000 in your browser")
        print("   🛑 Press Ctrl+C to stop the server")
        print()
        
        # Run Flask app
        subprocess.run([sys.executable, "app.py"])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Application error: {e}")

def main():
    """Main runner function"""
    print_banner()
    
    # Menu system
    while True:
        print("📋 What would you like to do?")
        print("1. Check requirements and setup")
        print("2. Train the AI model")
        print("3. Run the web application")
        print("4. Full setup and run")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\n" + "="*40)
            check_requirements()
            check_dataset()
            check_model()
            setup_database()
            print("="*40 + "\n")
            
        elif choice == '2':
            print("\n" + "="*40)
            if train_model():
                print("🎉 Training completed!")
            else:
                print("💥 Training failed!")
            print("="*40 + "\n")
            
        elif choice == '3':
            print("\n" + "="*40)
            run_application()
            print("="*40 + "\n")
            
        elif choice == '4':
            print("\n" + "="*40)
            print("🔄 Running complete setup...")
            
            # Check everything
            if not check_requirements():
                print("❌ Please install requirements first: pip install -r requirements.txt")
                continue
                
            if not check_dataset():
                print("❌ Please setup dataset first")
                continue
                
            # Train model if needed
            if not check_model():
                print("🎯 Training model...")
                if not train_model():
                    print("❌ Training failed!")
                    continue
            
            # Setup database
            setup_database()
            
            # Run application
            print("🚀 Starting application...")
            run_application()
            print("="*40 + "\n")
            
        elif choice == '5':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
