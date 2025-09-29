"""
Gemini AI Integration for Cattle Breed Recognition System
Provides enhanced breed insights and contextual information using Google's Gemini AI
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
import time

class GeminiAI:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini AI client
        
        Args:
            api_key: Google AI Studio API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
        if not self.api_key:
            print("⚠️  Gemini API key not found. Set GEMINI_API_KEY environment variable.")
            print("   Get your API key from: https://aistudio.google.com/app/apikey")
            self.enabled = False
        else:
            self.enabled = True
            print("✅ Gemini AI initialized successfully")
    
    def is_enabled(self) -> bool:
        """Check if Gemini AI is properly configured"""
        return self.enabled and bool(self.api_key)
    
    def generate_content(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """
        Generate content using Gemini AI
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text or None if error
        """
        if not self.is_enabled():
            return None
            
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            
            data = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.7
                }
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    return content.strip()
            else:
                print(f"❌ Gemini API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Gemini AI error: {str(e)}")
            
        return None
    
    def get_breed_insights(self, breed_name: str, confidence: float) -> Dict[str, Any]:
        """
        Get enhanced insights about a cattle breed using Gemini AI
        
        Args:
            breed_name: Name of the cattle breed
            confidence: Model confidence score
            
        Returns:
            Dictionary with breed insights
        """
        if not self.is_enabled():
            return {
                "enhanced_info": "Gemini AI not configured",
                "farming_tips": [],
                "health_considerations": [],
                "market_value": "Information not available"
            }
        
        prompt = f"""
        Provide detailed information about the {breed_name} cattle breed. Include:
        
        1. Key characteristics and appearance
        2. Origin and history
        3. Primary uses (dairy, beef, dual-purpose)
        4. Farming and care tips
        5. Health considerations
        6. Market value and commercial importance
        7. Adaptability to different climates
        
        Format the response as detailed but concise information that would be useful for farmers and livestock professionals.
        """
        
        try:
            response = self.generate_content(prompt, max_tokens=800)
            if response:
                return {
                    "enhanced_info": response,
                    "confidence_level": confidence,
                    "ai_enhanced": True,
                    "timestamp": time.time()
                }
        except Exception as e:
            print(f"❌ Error getting breed insights: {str(e)}")
        
        return {
            "enhanced_info": f"Basic information available for {breed_name}",
            "ai_enhanced": False,
            "error": "Could not fetch enhanced insights"
        }
    
    def analyze_prediction_context(self, prediction_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze prediction results and provide contextual insights
        
        Args:
            prediction_results: Results from ML model prediction
            
        Returns:
            Enhanced analysis with context
        """
        if not self.is_enabled():
            return {"analysis": "Gemini AI not available for analysis"}
        
        breed = prediction_results.get('breed', 'Unknown')
        confidence = prediction_results.get('confidence', 0.0)
        
        prompt = f"""
        A cattle breed recognition AI has identified a cow as "{breed}" with {confidence:.2%} confidence.
        
        Please provide:
        1. Assessment of the confidence level - is this a reliable identification?
        2. What factors might affect breed identification accuracy?
        3. Recommendations for the farmer based on this identification
        4. Suggestions for improving breed identification in future
        
        Keep the response practical and farmer-friendly.
        """
        
        try:
            analysis = self.generate_content(prompt, max_tokens=400)
            if analysis:
                return {
                    "contextual_analysis": analysis,
                    "confidence_assessment": self._assess_confidence(confidence),
                    "recommendations": self._get_recommendations(breed, confidence),
                    "ai_enhanced": True
                }
        except Exception as e:
            print(f"❌ Error analyzing prediction: {str(e)}")
        
        return {
            "contextual_analysis": "Basic prediction analysis available",
            "ai_enhanced": False
        }
    
    def _assess_confidence(self, confidence: float) -> str:
        """Assess confidence level"""
        if confidence >= 0.9:
            return "Very High - Strong identification"
        elif confidence >= 0.75:
            return "High - Reliable identification"
        elif confidence >= 0.6:
            return "Moderate - Consider additional verification"
        elif confidence >= 0.4:
            return "Low - Multiple possibilities exist"
        else:
            return "Very Low - Identification uncertain"
    
    def _get_recommendations(self, breed: str, confidence: float) -> List[str]:
        """Get basic recommendations based on breed and confidence"""
        recommendations = []
        
        if confidence < 0.6:
            recommendations.append("Consider taking multiple photos from different angles")
            recommendations.append("Ensure good lighting and clear view of the animal")
            recommendations.append("Consult with a veterinarian or livestock expert")
        
        recommendations.append(f"Research {breed} breed characteristics for verification")
        recommendations.append("Consider genetic testing for definitive breed identification")
        
        return recommendations
    
    def get_farming_advice(self, breed_name: str, context: str = "") -> Dict[str, Any]:
        """
        Get specific farming advice for a cattle breed
        
        Args:
            breed_name: Name of the cattle breed
            context: Additional context (location, purpose, etc.)
            
        Returns:
            Farming advice and tips
        """
        if not self.is_enabled():
            return {"advice": "Gemini AI not available for farming advice"}
        
        prompt = f"""
        Provide specific farming advice for {breed_name} cattle. Include:
        
        1. Feeding requirements and nutrition
        2. Housing and shelter needs
        3. Health monitoring and common issues
        4. Breeding considerations
        5. Economic aspects and profitability
        6. Seasonal care requirements
        
        {f"Additional context: {context}" if context else ""}
        
        Make the advice practical and actionable for farmers.
        """
        
        try:
            advice = self.generate_content(prompt, max_tokens=600)
            if advice:
                return {
                    "farming_advice": advice,
                    "breed": breed_name,
                    "ai_generated": True,
                    "timestamp": time.time()
                }
        except Exception as e:
            print(f"❌ Error getting farming advice: {str(e)}")
        
        return {
            "farming_advice": f"Basic farming guidelines available for {breed_name}",
            "ai_generated": False
        }

# Global Gemini AI instance
gemini_ai = GeminiAI()

def get_gemini_client() -> GeminiAI:
    """Get the global Gemini AI client"""
    return gemini_ai

def test_gemini_connection() -> Dict[str, Any]:
    """Test Gemini AI connection and functionality"""
    client = get_gemini_client()
    
    if not client.is_enabled():
        return {
            "status": "disabled",
            "message": "Gemini AI not configured. Set GEMINI_API_KEY environment variable.",
            "setup_url": "https://aistudio.google.com/app/apikey"
        }
    
    # Test with a simple prompt
    try:
        test_response = client.generate_content("Say 'Gemini AI is working correctly for cattle breed recognition'")
        if test_response:
            return {
                "status": "connected",
                "message": "Gemini AI is working correctly",
                "test_response": test_response[:100] + "..." if len(test_response) > 100 else test_response
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Connection test failed: {str(e)}"
        }
    
    return {
        "status": "error",
        "message": "Failed to get response from Gemini AI"
    }

if __name__ == "__main__":
    # Test the Gemini AI integration
    print("🧪 Testing Gemini AI Integration...")
    result = test_gemini_connection()
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    
    if result['status'] == 'connected':
        print("✅ Gemini AI integration is working!")
    else:
        print("⚠️  Gemini AI integration needs configuration")