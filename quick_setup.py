#!/usr/bin/env python3
"""
Quick setup for Breast Cancer Detection System
"""

import os
import sys
import subprocess

def check_and_install():
    """Check requirements and install if needed"""
    print("Checking and installing requirements...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install requirements")
        return False

def setup_directories():
    """Create necessary directories"""
    directories = [
        'models',
        'static/uploads',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def main():
    print("=" * 50)
    print("BREAST CANCER DETECTION SYSTEM - QUICK SETUP")
    print("=" * 50)
    
    # Setup directories
    setup_directories()
    
    # Install requirements
    if check_and_install():
        print("\nSetup completed successfully!")
        print("\nNext steps:")
        print("1. Setup MySQL database: mysql -u root -p < database_setup.sql")
        print("2. Train model: python enhanced_train.py")
        print("3. Run app: python app.py")
    else:
        print("\nSetup failed. Please check requirements.txt")

if __name__ == "__main__":
    main()
