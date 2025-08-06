#!/usr/bin/env python3
"""
CI/CD API Test Script

This script tests the API endpoints in the CI/CD environment.
It starts the API server, tests it, and then stops it.
"""

import requests
import json
import time
import sys
import os
import subprocess
import signal
from pathlib import Path

def check_models_exist():
    """Check if model files exist"""
    print("Checking model files...")
    
    required_models = [
        "models/LinearRegression.pkl",
        "models/DecisionTree.pkl",
        "models/LogisticRegression.pkl",
        "models/RandomForest.pkl"
    ]
    
    all_exist = True
    for model_path in required_models:
        if os.path.exists(model_path):
            print(f"✅ {model_path} exists")
        else:
            print(f"❌ {model_path} missing")
            all_exist = False
    
    return all_exist

def start_api_server():
    """Start the API server"""
    print("Starting API server...")
    
    # Start the server in the background
    process = subprocess.Popen([
        "python", "-m", "uvicorn", "api.housing_api:app", 
        "--host", "0.0.0.0", "--port", "8000"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(10)
    
    return process

def test_housing_api():
    """Test the housing prediction API"""
    print("Testing Housing API...")
    
    # Test data for housing prediction
    test_data = {
        "total_rooms": 8.0,
        "total_bedrooms": 3.0,
        "population": 1000.0,
        "households": 500.0,
        "median_income": 3.5,
        "housing_median_age": 35.0,
        "latitude": 37.7749,
        "longitude": -122.4194
    }
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            print("✅ Housing API health check passed")
        else:
            print(f"❌ Housing API health check failed: {response.status_code}")
            return False
        
        # Test metrics endpoint
        response = requests.get("http://localhost:8000/metrics", timeout=10)
        if response.status_code == 200:
            print("✅ Housing API metrics endpoint working")
        else:
            print(f"❌ Housing API metrics failed: {response.status_code}")
            return False
        
        # Test prediction endpoint
        response = requests.post(
            "http://localhost:8000/predict",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if "predicted_price" in result:
                print(f"✅ Housing API prediction working: {result['predicted_price']}")
            else:
                print("❌ Housing API prediction response format incorrect")
                return False
        else:
            print(f"❌ Housing API prediction failed: {response.status_code}")
            return False
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Housing API test failed: {e}")
        return False

def stop_api_server(process):
    """Stop the API server"""
    print("Stopping API server...")
    process.terminate()
    process.wait()

def main():
    """Main test function"""
    print("=" * 50)
    print("CI/CD API TESTING SCRIPT")
    print("=" * 50)
    
    # Check if models exist
    models_ok = check_models_exist()
    if not models_ok:
        print("❌ Some model files are missing")
        sys.exit(1)
    
    # Start API server
    api_process = start_api_server()
    
    try:
        # Test housing API
        housing_ok = test_housing_api()
        
        print("=" * 50)
        if housing_ok:
            print("✅ Housing API tests passed!")
            sys.exit(0)
        else:
            print("❌ Housing API tests failed!")
            sys.exit(1)
    
    finally:
        # Always stop the server
        stop_api_server(api_process)

if __name__ == "__main__":
    main() 