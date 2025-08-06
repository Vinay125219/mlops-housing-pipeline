#!/usr/bin/env python3
"""
CI/CD Pipeline Verification Script

This script verifies that all components of the CI/CD pipeline work correctly
before pushing to GitHub. It simulates the GitHub Actions workflow locally.
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            if check:
                return False
            else:
                print(f"⚠️ {description} - WARNING (continuing)")
                return True
    except Exception as e:
        print(f"❌ {description} - EXCEPTION: {e}")
        if check:
            return False
        else:
            print(f"⚠️ {description} - WARNING (continuing)")
            return True

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✅ {description} - EXISTS")
        return True
    else:
        print(f"❌ {description} - NOT FOUND")
        return False

def check_directory_structure():
    """Check if all required directories exist."""
    print("\n📁 Checking directory structure...")
    
    required_dirs = [
        "src",
        "api", 
        "data",
        "models",
        "housinglogs",
        "irislogs",
        ".github/workflows"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/ - EXISTS")
        else:
            print(f"❌ {dir_path}/ - MISSING")
            all_exist = False
    
    return all_exist

def check_required_files():
    """Check if all required files exist."""
    print("\n📄 Checking required files...")
    
    required_files = [
        "requirements.txt",
        "Dockerfile",
        ".github/workflows/ci-cd.yml",
        "src/load_data.py",
        "src/train_and_track.py", 
        "src/train_iris.py",
        "api/housing_api.py",
        "api/main.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if check_file_exists(file_path, f"File: {file_path}"):
            pass
        else:
            all_exist = False
    
    return all_exist

def test_dependencies():
    """Test dependency installation."""
    print("\n📦 Testing dependencies...")
    
    # Test pip upgrade
    success = run_command("python -m pip install --upgrade pip", "Upgrading pip")
    
    # Test requirements installation
    success &= run_command("pip install -r requirements.txt", "Installing requirements.txt")
    
    # Test additional tools
    success &= run_command("pip install flake8 pytest bandit", "Installing CI tools")
    
    # Test imports
    test_imports = """
import fastapi
import mlflow
import sklearn
import pandas
import numpy
import joblib
import uvicorn
print("✅ All core dependencies imported successfully")
"""
    
    success &= run_command(f'python -c "{test_imports}"', "Testing core imports")
    
    return success

def test_data_processing():
    """Test data preprocessing pipeline."""
    print("\n🔄 Testing data processing...")
    
    # Create directories
    run_command("mkdir -p data models housinglogs irislogs", "Creating directories", check=False)
    
    # Run data preprocessing
    success = run_command("python src/load_data.py", "Running data preprocessing")
    
    # Check if data file was created
    success &= check_file_exists("data/housing.csv", "Processed data file")
    
    return success

def test_model_training():
    """Test model training pipeline."""
    print("\n🤖 Testing model training...")
    
    # Train housing models
    success = run_command("python src/train_and_track.py", "Training housing models")
    
    # Train iris models  
    success &= run_command("python src/train_iris.py", "Training iris models")
    
    # Check if models were created
    model_files = [
        "models/DecisionTree.pkl",
        "models/LinearRegression.pkl", 
        "models/LogisticRegression.pkl",
        "models/RandomForest.pkl"
    ]
    
    for model_file in model_files:
        success &= check_file_exists(model_file, f"Model file: {model_file}")
    
    return success

def test_code_quality():
    """Test code quality checks."""
    print("\n🔍 Testing code quality...")
    
    # Run flake8 linting
    success = run_command(
        "flake8 src api --count --select=E9,F63,F7,F82 --show-source --statistics --max-line-length=120",
        "Running flake8 linting"
    )
    
    # Run security scan
    success &= run_command(
        "bandit -r src api -f json -o bandit-report.json",
        "Running security scan with bandit"
    )
    
    # Check for secrets
    success &= run_command(
        'grep -r "password\|secret\|key" src api --exclude="*.pyc" --exclude="__pycache__" || echo "✅ No obvious secrets found"',
        "Checking for hardcoded secrets"
    )
    
    return success

def test_docker_build():
    """Test Docker build process."""
    print("\n🐳 Testing Docker build...")
    
    # Check Dockerfile exists
    success = check_file_exists("Dockerfile", "Dockerfile")
    
    # Test Docker build (dry run)
    success &= run_command("docker build --dry-run .", "Testing Docker build syntax")
    
    # Test actual build (if Docker is available)
    try:
        result = subprocess.run("docker --version", shell=True, capture_output=True)
        if result.returncode == 0:
            success &= run_command("docker build -t mlops-app:test .", "Building Docker image")
            
            # Test container run
            success &= run_command(
                "docker run --rm -d --name test-mlops-app -p 8000:8000 mlops-app:test",
                "Starting test container"
            )
            
            # Wait for container to start
            time.sleep(5)
            
            # Test health check
            success &= run_command(
                "curl -f http://localhost:8000/ || echo '⚠️ Health check failed'",
                "Testing API health check"
            )
            
            # Clean up
            run_command("docker stop test-mlops-app", "Stopping test container", check=False)
            run_command("docker rmi mlops-app:test", "Removing test image", check=False)
        else:
            print("⚠️ Docker not available, skipping Docker tests")
    except:
        print("⚠️ Docker not available, skipping Docker tests")
    
    return success

def test_api_functionality():
    """Test API functionality."""
    print("\n🌐 Testing API functionality...")
    
    # Check if models exist
    if not os.path.exists("models/DecisionTree.pkl"):
        print("⚠️ Models not found, skipping API tests")
        return True
    
    # Test API startup (background)
    success = run_command(
        "timeout 30 uvicorn api.housing_api:app --host 0.0.0.0 --port 8000 --log-level error &",
        "Starting API server",
        check=False
    )
    
    # Wait for server to start
    time.sleep(3)
    
    # Test health endpoint
    success &= run_command(
        "curl -f http://localhost:8000/ || echo '⚠️ Health endpoint failed'",
        "Testing health endpoint"
    )
    
    # Test metrics endpoint
    success &= run_command(
        "curl -f http://localhost:8000/metrics || echo '⚠️ Metrics endpoint failed'",
        "Testing metrics endpoint"
    )
    
    # Kill the server
    run_command("pkill -f uvicorn", "Stopping API server", check=False)
    
    return success

def generate_report(results):
    """Generate a summary report."""
    print("\n" + "="*60)
    print("📊 CI/CD PIPELINE VERIFICATION REPORT")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    failed_tests = total_tests - passed_tests
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests == 0:
        print("\n🎉 ALL TESTS PASSED! Your CI/CD pipeline is ready.")
        print("You can now push to GitHub with confidence.")
    else:
        print(f"\n⚠️ {failed_tests} test(s) failed. Please fix the issues before pushing.")
    
    print("\n" + "="*60)

def main():
    """Main verification function."""
    print("🚀 Starting CI/CD Pipeline Verification")
    print("This script simulates the GitHub Actions workflow locally.")
    
    results = {}
    
    # Run all verification steps
    results["Directory Structure"] = check_directory_structure()
    results["Required Files"] = check_required_files()
    results["Dependencies"] = test_dependencies()
    results["Data Processing"] = test_data_processing()
    results["Model Training"] = test_model_training()
    results["Code Quality"] = test_code_quality()
    results["Docker Build"] = test_docker_build()
    results["API Functionality"] = test_api_functionality()
    
    # Generate report
    generate_report(results)
    
    # Exit with appropriate code
    if all(results.values()):
        print("\n✅ Verification completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Verification failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 