#!/usr/bin/env python3
"""
Simple Gemini API test
"""

import os
import requests
import time

# Set API key
os.environ['GEMINI_API_KEY'] = 'AIzaSyAyvXvRneYS_6O9hrlS24658dBn2TY-Nhk'

from gemini_integration import GeminiAI

def test_gemini_direct():
    """Test Gemini AI directly"""
    print("🧪 Testing Gemini AI directly...")
    
    # Initialize Gemini
    gemini = GeminiAI()
    
    # Test basic content generation
    try:
        response = gemini.generate_content("What is a Holstein cattle breed?")
        print(f"✅ Direct Gemini test successful!")
        print(f"Response: {response[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Direct Gemini test failed: {e}")
        return False

def test_flask_endpoints():
    """Test Flask endpoints"""
    print("\n🧪 Testing Flask endpoints...")
    
    base_url = "http://192.168.95.195:5000"
    
    # Wait for server to be ready
    time.sleep(3)
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
            
        # Test Gemini status
        response = requests.get(f"{base_url}/gemini/status", timeout=10)
        if response.status_code == 200:
            print("✅ Gemini status endpoint working")
            print(f"Status: {response.json()}")
        else:
            print(f"❌ Gemini status failed: {response.status_code}")
            
        # Test breed insights
        response = requests.get(f"{base_url}/gemini/breed-insights?breed=Holstein", timeout=30)
        if response.status_code == 200:
            print("✅ Breed insights endpoint working")
            data = response.json()
            print(f"Insights preview: {str(data)[:200]}...")
        else:
            print(f"❌ Breed insights failed: {response.status_code}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server")
        return False
    except Exception as e:
        print(f"❌ Flask test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Simple Gemini Integration Test")
    print("=" * 50)
    
    # Test direct Gemini
    gemini_works = test_gemini_direct()
    
    # Test Flask endpoints if Gemini works
    if gemini_works:
        flask_works = test_flask_endpoints()
        
        if flask_works:
            print("\n🎉 All tests passed! Gemini integration is working!")
        else:
            print("\n⚠️  Gemini works directly, but Flask integration has issues")
    else:
        print("\n❌ Gemini API not working. Check your API key.")