#!/usr/bin/env python3
"""
Test Flask API with mobile app image format
"""

import requests
import os

def test_flask_api():
    base_url = "http://192.168.95.195:5000"
    
    print("🧪 Testing Flask API endpoints...")
    
    # Test health
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test breeds endpoint
    try:
        response = requests.get(f"{base_url}/breeds")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Breeds endpoint working - {data.get('count', 0)} breeds available")
        else:
            print(f"❌ Breeds endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Breeds endpoint error: {e}")
    
    # Test Gemini status
    try:
        response = requests.get(f"{base_url}/gemini/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Gemini status: {data.get('status', 'unknown')}")
        else:
            print(f"❌ Gemini status failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Gemini status error: {e}")

if __name__ == "__main__":
    test_flask_api()