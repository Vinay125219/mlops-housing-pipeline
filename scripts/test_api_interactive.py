#!/usr/bin/env python3
"""
Interactive API Testing Script
This script allows you to test the MLOps Housing API interactively
"""

import requests
import json
import time
from typing import Dict, Any

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health(self) -> bool:
        """Test the health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                print(f"✅ Health check passed: {response.json()}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_prediction(self, data: Dict[str, Any]) -> bool:
        """Test the prediction endpoint"""
        try:
            response = self.session.post(
                f"{self.base_url}/predict",
                json=data,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Prediction successful: ${result.get('predicted_price', 'N/A'):,.2f}")
                return True
            else:
                print(f"❌ Prediction failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return False
    
    def test_metrics(self) -> bool:
        """Test the metrics endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/metrics")
            if response.status_code == 200:
                metrics = response.json()
                print(f"✅ Metrics retrieved: {metrics}")
                return True
            else:
                print(f"❌ Metrics failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Metrics error: {e}")
            return False
    
    def run_interactive_tests(self):
        """Run interactive API tests"""
        print("🚀 MLOps Housing API Interactive Tester")
        print("=" * 50)
        
        # Test health
        print("\n1. Testing Health Endpoint...")
        if not self.test_health():
            print("❌ Cannot proceed - API is not healthy")
            return
        
        # Test metrics before predictions
        print("\n2. Testing Metrics Endpoint...")
        self.test_metrics()
        
        # Sample test cases
        test_cases = [
            {
                "name": "Luxury Home",
                "data": {
                    "total_rooms": 12.0,
                    "total_bedrooms": 5.0,
                    "population": 2000.0,
                    "households": 800.0,
                    "median_income": 8.5,
                    "housing_median_age": 25.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194
                }
            },
            {
                "name": "Affordable Home",
                "data": {
                    "total_rooms": 4.0,
                    "total_bedrooms": 2.0,
                    "population": 500.0,
                    "households": 200.0,
                    "median_income": 2.0,
                    "housing_median_age": 45.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194
                }
            },
            {
                "name": "Medium Home",
                "data": {
                    "total_rooms": 8.0,
                    "total_bedrooms": 3.0,
                    "population": 1000.0,
                    "households": 500.0,
                    "median_income": 3.5,
                    "housing_median_age": 35.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194
                }
            }
        ]
        
        print("\n3. Testing Prediction Endpoints...")
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n   Test {i}: {test_case['name']}")
            print(f"   Input: {json.dumps(test_case['data'], indent=2)}")
            self.test_prediction(test_case['data'])
            time.sleep(1)  # Small delay between requests
        
        # Test metrics after predictions
        print("\n4. Testing Metrics After Predictions...")
        self.test_metrics()
        
        print("\n🎉 Interactive testing completed!")
        print(f"📖 API Documentation: {self.base_url}/docs")
        print(f"🌐 Health Check: {self.base_url}/")

def main():
    """Main function to run interactive API tests"""
    print("Starting Interactive API Tester...")
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code != 200:
            print("❌ API is not running. Please start the application first:")
            print("   docker run -d --name mlops-production -p 8000:8000 mlops-app:latest")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Please ensure:")
        print("   1. The application is running on port 8000")
        print("   2. Docker container is started: docker start mlops-production")
        print("   3. Or start fresh: docker run -d --name mlops-production -p 8000:8000 mlops-app:latest")
        return
    
    # Run tests
    tester = APITester()
    tester.run_interactive_tests()

if __name__ == "__main__":
    main() 