#!/usr/bin/env python3
"""
Direct Gemini API test
"""

import requests
import json

API_KEY = "AIzaSyAyvXvRneYS_6O9hrlS24658dBn2TY-Nhk"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

def test_gemini_api():
    """Test Gemini API directly"""
    print("🧪 Testing Gemini API directly...")
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": "What is a Holstein cattle breed? Keep it brief."
            }]
        }]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}?key={API_KEY}",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            print(f"✅ Gemini API working!")
            print(f"Response: {content}")
            return True
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    test_gemini_api()