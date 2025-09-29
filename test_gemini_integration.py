"""
Test script for Gemini AI integration in Cattle Breed Recognition System
"""

import requests
import json
import time

# Test configuration
BASE_URL = "http://192.168.95.195:5000"

def test_basic_endpoints():
    """Test basic API endpoints"""
    print("🧪 Testing Basic API Endpoints...")
    
    # Test health
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Health Check: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Model Loaded: {data.get('model_loaded', False)}")
        print(f"   Classes: {data.get('num_classes', 0)}")
    
    # Test breeds
    response = requests.get(f"{BASE_URL}/breeds")
    print(f"✅ Breeds Endpoint: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Available Breeds: {data.get('count', 0)}")
        print(f"   Sample Breeds: {data.get('breeds', [])[:5]}")

def test_gemini_endpoints():
    """Test Gemini AI integration endpoints"""
    print("\n🤖 Testing Gemini AI Integration...")
    
    # Test Gemini status
    try:
        response = requests.get(f"{BASE_URL}/gemini/status")
        print(f"✅ Gemini Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Message: {data.get('message', 'No message')}")
            if 'setup_url' in data:
                print(f"   Setup URL: {data['setup_url']}")
    except Exception as e:
        print(f"❌ Gemini Status Error: {e}")
    
    # Test breed insights (will return "not configured" message)
    try:
        response = requests.get(f"{BASE_URL}/gemini/breed-insights/Holstein")
        print(f"✅ Breed Insights: {response.status_code}")
        if response.status_code == 503:  # Service unavailable (expected without API key)
            data = response.json()
            print(f"   Expected: {data.get('message', 'Not configured')}")
        elif response.status_code == 200:
            data = response.json()
            print(f"   AI Enhanced: {data.get('ai_enhanced', False)}")
    except Exception as e:
        print(f"❌ Breed Insights Error: {e}")
    
    # Test farming advice
    try:
        payload = {"context": "Small farm in temperate climate"}
        response = requests.post(f"{BASE_URL}/gemini/farming-advice/Holstein", json=payload)
        print(f"✅ Farming Advice: {response.status_code}")
        if response.status_code == 503:  # Service unavailable (expected without API key)
            data = response.json()
            print(f"   Expected: {data.get('message', 'Not configured')}")
        elif response.status_code == 200:
            data = response.json()
            print(f"   AI Generated: {data.get('ai_generated', False)}")
    except Exception as e:
        print(f"❌ Farming Advice Error: {e}")

def test_backend_integration():
    """Test Express.js backend integration"""
    print("\n🔗 Testing Backend Integration...")
    
    try:
        response = requests.get("http://192.168.95.195:3000/test-flask")
        print(f"✅ Backend → Flask: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Integration: {data.get('status', 'unknown')}")
            flask_response = data.get('flaskResponse', {})
            print(f"   Flask Model: {flask_response.get('model_loaded', False)}")
            print(f"   Flask Classes: {flask_response.get('num_classes', 0)}")
    except Exception as e:
        print(f"❌ Backend Integration Error: {e}")

def print_gemini_setup_info():
    """Print setup information for Gemini AI"""
    print("\n" + "="*60)
    print("🔧 GEMINI AI SETUP INSTRUCTIONS")
    print("="*60)
    print("1. Get API Key:")
    print("   → Go to: https://aistudio.google.com/app/apikey")
    print("   → Sign in and create a new API key")
    print()
    print("2. Set Environment Variable:")
    print("   PowerShell: $env:GEMINI_API_KEY=\"your-api-key-here\"")
    print("   CMD: set GEMINI_API_KEY=your-api-key-here")
    print()
    print("3. Restart Flask Server:")
    print("   → Stop current server (Ctrl+C)")
    print("   → Run: python flask_api.py")
    print()
    print("4. Test Enhanced Features:")
    print("   → POST /predict-enhanced (ML + AI insights)")
    print("   → GET /gemini/breed-insights/{breed}")
    print("   → POST /gemini/farming-advice/{breed}")
    print("="*60)

def main():
    """Run all tests"""
    print("🚀 Cattle Breed Recognition System - Gemini AI Integration Test")
    print("="*70)
    
    # Test basic functionality
    test_basic_endpoints()
    
    # Test Gemini integration
    test_gemini_endpoints()
    
    # Test backend integration
    test_backend_integration()
    
    # Show setup info
    print_gemini_setup_info()
    
    print("\n✅ Integration Test Complete!")
    print("📱 Your mobile app can now use enhanced predictions with AI insights")
    print("🧠 Configure Gemini API key to unlock AI-powered features")

if __name__ == "__main__":
    main()