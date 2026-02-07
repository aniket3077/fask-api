"""
Gemini AI Integration for Cattle Breed Recognition System
Provides enhanced breed insights and contextual information using Google's Gemini AI
"""

import os
import json
import requests
import base64
from typing import Dict, List, Optional, Any, Tuple
import time

class GeminiAI:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini AI client via OpenRouter
        
        Args:
            api_key: OpenRouter API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model_vision = "google/gemini-2.0-flash-exp:free"  # Free vision model
        self.model_text = "google/gemini-2.0-flash-exp:free"    # Free text model
        
        if not self.api_key:
            print("⚠️  OpenRouter API key not found. Set GEMINI_API_KEY environment variable.")
            print("   Get your API key from: https://openrouter.ai/keys")
            self.enabled = False
        else:
            self.enabled = True
            print("✅ Gemini AI (via OpenRouter) initialized successfully")
    
    def is_enabled(self) -> bool:
        """Check if Gemini AI is properly configured"""
        return self.enabled and bool(self.api_key)
    
    def analyze_image_for_cow(self, image_bytes: bytes) -> Tuple[bool, str]:
        """
        Analyze image to determine if it contains a cow.
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Tuple of (is_cow: bool, message: str)
        """
        if not self.is_enabled():
            return True, "Gemini AI not configured - skipping cow validation"
        
        try:
            # Convert image to base64
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Prepare request for OpenRouter
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}',
                'HTTP-Referer': 'http://localhost:5000',
                'X-Title': 'Cattle Breed Recognition'
            }
            
            data = {
                "model": self.model_vision,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Is there a cow or cattle animal visible in this image? Respond with ONLY 'YES' if you clearly see a cow/cattle/bovine, or 'NO' if you see something else (like a dog, cat, person, or any non-cattle animal/object). After YES or NO, add a hyphen and brief reason."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 100,
                "temperature": 0.1
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    text = result['choices'][0]['message']['content'].strip()
                    
                    # Parse response
                    text_upper = text.upper()
                    if text_upper.startswith('YES'):
                        reason = text.split('-', 1)[1].strip() if '-' in text else "Cow detected"
                        return True, f"Valid cow image: {reason}"
                    elif text_upper.startswith('NO'):
                        reason = text.split('-', 1)[1].strip() if '-' in text else "Not a cow"
                        return False, f"This image does not contain a cow. {reason}"
                    else:
                        # Unclear response
                        return False, f"Could not verify cow in image. AI response: {text}"
            else:
                print(f"❌ OpenRouter Vision API error: {response.status_code}")
                error_text = response.json() if response.text else {}
                print(f"Error details: {error_text}")
                # Fail open - allow image through if API fails
                return True, f"Cow validation service temporarily unavailable"
                
        except Exception as e:
            print(f"❌ Cow detection error: {str(e)}")
            # Fail open - allow image through if error occurs
            return True, f"Cow validation error: {str(e)}"
        
        return True, "Cow validation completed"
    
    def generate_content(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """
        Generate content using Gemini AI via OpenRouter
        
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
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}',
                'HTTP-Referer': 'http://localhost:5000',
                'X-Title': 'Cattle Breed Recognition'
            }
            
            data = {
                "model": self.model_text,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    return content.strip()
            else:
                print(f"❌ OpenRouter API error: {response.status_code} - {response.text}")
                
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

# Global Gemini AI instance (will be initialized lazily)
gemini_ai = None

def get_gemini_client() -> GeminiAI:
    """Get the global Gemini AI client (lazy initialization)"""
    global gemini_ai
    if gemini_ai is None:
        gemini_ai = GeminiAI()
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