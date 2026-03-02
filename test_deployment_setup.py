#!/usr/bin/env python3
"""
Test script to verify deployment setup and model loading
"""

import os
import sys
from app_production import load_model, model, classes

def test_model_loading():
    """Test model loading with detailed diagnostics"""
    print("=" * 60)
    print("TESTING MODEL LOADING")
    print("=" * 60)
    
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}...")  # Show first 3 entries
    
    # Check model file existence
    model_paths = [
        os.path.join(os.getcwd(), 'models', 'densenet121_model.h5'),
        os.path.join(os.path.dirname(__file__), 'models', 'densenet121_model.h5'),
        '/var/task/models/densenet121_model.h5',
        'models/densenet121_model.h5'
    ]
    
    print("\nChecking model file locations:")
    for path in model_paths:
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        print(f"  {path}: {'EXISTS' if exists else 'MISSING'} ({size:,} bytes)" if exists else f"  {path}: MISSING")
    
    # Test model loading
    print("\nTesting model loading...")
    success = load_model()
    
    if success:
        print("Model loaded successfully!")
        print(f"   Model type: {type(model)}")
        print(f"   Classes: {classes}")
        if hasattr(model, 'input_shape'):
            print(f"   Input shape: {model.input_shape}")
        if hasattr(model, 'output_shape'):
            print(f"   Output shape: {model.output_shape}")
    else:
        print("Model loading failed!")
        print(f"   Model variable: {model}")
    
    return success

def test_file_structure():
    """Test required file structure"""
    print("\n" + "=" * 60)
    print("TESTING FILE STRUCTURE")
    print("=" * 60)
    
    required_files = [
        'app_production.py',
        'api/index.py',
        'api/__init__.py',
        'vercel.json',
        'requirements.txt',
        'models/densenet121_model.h5'
    ]
    
    print("Checking required files:")
    all_exist = True
    for file_path in required_files:
        exists = os.path.exists(file_path)
        print(f"  {file_path}: {'EXISTS' if exists else 'MISSING'}")
        if not exists:
            all_exist = False
    
    return all_exist

def test_vercel_config():
    """Test Vercel configuration"""
    print("\n" + "=" * 60)
    print("TESTING VERCEL CONFIGURATION")
    print("=" * 60)
    
    try:
        import json
        with open('vercel.json', 'r') as f:
            config = json.load(f)
        
        print("Vercel configuration:")
        print(f"  Version: {config.get('version')}")
        print(f"  Python version: {config.get('env', {}).get('PYTHON_VERSION')}")
        print(f"  Builds: {len(config.get('builds', []))}")
        print(f"  Function timeout: {config.get('functions', {}).get('api/index.py', {}).get('maxDuration', 'default')} seconds")
        
        return True
    except Exception as e:
        print(f"Error reading vercel.json: {e}")
        return False

if __name__ == "__main__":
    print("DEPLOYMENT SETUP VERIFICATION")
    print("This script tests the setup for Vercel deployment")
    
    # Run all tests
    model_ok = test_model_loading()
    structure_ok = test_file_structure()
    config_ok = test_vercel_config()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    print(f"Model Loading: {'PASS' if model_ok else 'FAIL'}")
    print(f"File Structure: {'PASS' if structure_ok else 'FAIL'}")
    print(f"Vercel Config: {'PASS' if config_ok else 'FAIL'}")
    
    if model_ok and structure_ok and config_ok:
        print("\nAll tests passed! Ready for deployment.")
        sys.exit(0)
    else:
        print("\nSome tests failed. Please fix issues before deploying.")
        sys.exit(1)
