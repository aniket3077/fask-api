#!/usr/bin/env python3
"""
# This file will be moved to flask-api directory
Updated to work with Express.js backend.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pathlib import Path
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
import time
import base64
from dotenv import load_dotenv
from breed_info import get_breed_info, get_all_breeds
from gemini_integration import get_gemini_client, test_gemini_connection

# Load environment variables
load_dotenv()

# ======================================================================================
# 1. APPLICATION SETUP & MODEL LOADING
# ======================================================================================

app = Flask(__name__)
CORS(app)  # Enable CORS for Express.js backend
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB upload limit

# Global variables
MODEL = None
CLASS_NAMES = None
DEVICE = "cpu"

def get_device():
    """Gets the best available device for PyTorch."""
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")

def build_model(model_name, num_classes, pretrained=False):
    """Builds the model architecture."""
    if model_name == 'resnet18':
        model = models.resnet18(weights=None)
    elif model_name == 'resnet34':
        model = models.resnet34(weights=None)
    elif model_name == 'efficientnet_b0':
        model = models.efficientnet_b0(weights=None)
    else:
        raise ValueError(f"Model {model_name} not supported.")

    if 'resnet' in model_name:
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, num_classes)
    elif 'efficientnet' in model_name:
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)
    return model

def load_model():
    """Load the trained model and class names into memory."""
    global MODEL, CLASS_NAMES, DEVICE
    
    DEVICE = get_device()
    base_dir = Path(__file__).resolve().parent
    # Try multiple possible model locations
    model_paths = [
        base_dir / "__MACOSX" / "models" / "best_model.pth",  # Mac extracted path
        base_dir / "models" / "best_model.pth",  # Current path
        base_dir / "__MACOSX" / "models" / "bovine_model.pth"  # Alternative model
    ]
    
    model_path = None
    for path in model_paths:
        if path.is_file():
            model_path = path
            print(f"📁 Found model at: {model_path}")
            break
    
    if model_path is None:
        raise FileNotFoundError(f"Model not found in any of these locations: {model_paths}")
    
    model_name = "resnet18"
    
    if not model_path.is_file():
        raise FileNotFoundError(f"Model not found at: {model_path}")
        
    checkpoint = torch.load(model_path, map_location=DEVICE)
    CLASS_NAMES = checkpoint['class_names']
    num_classes = len(CLASS_NAMES)
    
    MODEL = build_model(model_name=model_name, num_classes=num_classes)
    MODEL.load_state_dict(checkpoint['model_state_dict'])
    MODEL.to(DEVICE)
    MODEL.eval()
    
    print(f"✅ Model loaded successfully on {DEVICE}")

def transform_image(image_bytes):
    """Apply transformations to the uploaded image."""
    image_size = 224
    transform = transforms.Compose([
        transforms.Resize(int(image_size * 1.14)),
        transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return transform(image).unsqueeze(0)

def get_prediction(image_tensor):
    """Get prediction from the model."""
    image_tensor = image_tensor.to(DEVICE)
    with torch.no_grad():
        outputs = MODEL(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        top_prob, top_idx = torch.topk(probabilities, 1)

    pred_class_name = CLASS_NAMES[top_idx[0].item()]
    confidence_score = top_prob[0].item()
    return pred_class_name, confidence_score

# ======================================================================================
# 2. API ROUTES FOR EXPRESS.JS INTEGRATION
# ======================================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    ready = MODEL is not None and CLASS_NAMES is not None
    return jsonify({
        'status': 'healthy' if ready else 'error',
        'version': '1.0.0',
        'mode': 'production',
        'device': str(DEVICE),
        'model_loaded': ready,
        'model_type': 'ResNet18' if ready else 'none',
        'num_classes': len(CLASS_NAMES) if CLASS_NAMES else 0,
        'timestamp': time.time()
    }), 200 if ready else 503

@app.route('/predict', methods=['POST'])
def predict():
    """Main prediction endpoint for Express.js backend."""
    start_time = time.time()
    
    try:
        # Check if we have class names (model loaded or demo mode)
        if CLASS_NAMES is None:
            return jsonify({
                'error': 'Service not ready. Please try again later.'
            }), 503

        # Handle both 'image' and 'file' keys for compatibility
        file = request.files.get('image') or request.files.get('file')
        
        if not file:
            return jsonify({
                'error': 'No image file provided. Use "image" field in form-data.'
            }), 400

        if file.filename == '':
            return jsonify({
                'error': 'No file selected'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Unsupported file type. Use JPG, JPEG, PNG, or WEBP.'
            }), 400

        # Read image bytes
        img_bytes = file.read()
        
        # STEP 1: Validate image format and quality
        is_valid, validation_message = validate_image(img_bytes)
        if not is_valid:
            return jsonify({
                'error': validation_message,
                'validation_failed': True
            }), 400
        
        print(f"✅ Image validation passed: {validation_message}")
        
        # STEP 2: Validate that image contains a cow
        is_cow, cow_message = validate_cow_image(img_bytes)
        if not is_cow:
            return jsonify({
                'error': f'Invalid image: {cow_message}',
                'validation_failed': True,
                'reason': 'not_a_cow'
            }), 400
        
        print(f"🐄 Cow validation passed: {cow_message}")

        # STEP 3: Process image through ML model
        tensor = transform_image(img_bytes)
        breed_name, confidence = get_prediction(tensor)
        
        processing_time = time.time() - start_time
        
        # Get breed information
        breed_info_data = get_breed_info(breed_name)
        
        # STEP 3: Enhance with Gemini AI insights
        gemini_insights = None
        gemini_client = get_gemini_client()
        
        if gemini_client and gemini_client.is_enabled():
            try:
                # Get AI-enhanced breed insights
                insights = gemini_client.get_breed_insights(breed_name, confidence)
                gemini_insights = insights
                print(f"✨ Gemini AI insights added for {breed_name}")
            except Exception as e:
                print(f"⚠️  Gemini AI error (non-critical): {str(e)}")
                gemini_insights = {'error': 'AI insights temporarily unavailable'}

        response = {
            'prediction': breed_name,
            'confidence': confidence,
            'processing_time': processing_time,
            'breed_info': breed_info_data,
            'timestamp': time.time(),
            'validation': 'passed'
        }
        
        if gemini_insights:
            response['ai_insights'] = gemini_insights
            response['enhanced'] = True
        
        return jsonify(response), 200

    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/breeds', methods=['GET'])
def get_breeds():
    """Get list of available breeds."""
    try:
        if CLASS_NAMES is None:
            return jsonify({'breeds': []}), 200
        
        return jsonify({
            'breeds': CLASS_NAMES,
            'count': len(CLASS_NAMES)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/breed-info/<breed_name>', methods=['GET'])
def get_breed_details(breed_name):
    """Get detailed information about a specific breed."""
    try:
        breed_info_data = get_breed_info(breed_name)
        if breed_info_data:
            return jsonify(breed_info_data), 200
        else:
            return jsonify({'error': 'Breed not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Detailed status endpoint."""
    return jsonify({
        'flask_status': 'running',
        'model_status': 'loaded' if MODEL is not None else 'not_loaded',
        'device': str(DEVICE),
        'available_breeds': len(CLASS_NAMES) if CLASS_NAMES else 0,
        'memory_usage': torch.cuda.memory_allocated() if torch.cuda.is_available() else 'N/A',
        'version': '1.0.0'
    }), 200

def allowed_file(filename: str) -> bool:
    """Validate allowed image extensions."""
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in {'jpg', 'jpeg', 'png', 'webp'}

def validate_image(image_bytes: bytes) -> tuple[bool, str]:
    """Validate if the uploaded file is a valid image.
    
    Args:
        image_bytes: Raw bytes of the uploaded file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if file is empty
    if len(image_bytes) == 0:
        return False, "Empty file uploaded"
    
    # Check file size (minimum 1KB, maximum 10MB)
    if len(image_bytes) < 1024:
        return False, "Image file too small. Minimum size is 1KB"
    
    if len(image_bytes) > 10 * 1024 * 1024:
        return False, "Image file too large. Maximum size is 10MB"
    
    # Try to open and validate with PIL
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # Verify it's an image by trying to load it
        image.verify()
        
        # Re-open for additional checks (verify() closes the image)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Check format
        image_format = image.format
        if image_format not in ['JPEG', 'PNG', 'WEBP']:
            return False, f"Invalid image format: {image_format}. Please upload JPEG, PNG, or WebP"
        
        # Check image dimensions (minimum 100x100, maximum 4000x4000)
        width, height = image.size
        if width < 100 or height < 100:
            return False, f"Image too small ({width}x{height}). Minimum size is 100x100 pixels"
        
        if width > 4000 or height > 4000:
            return False, f"Image too large ({width}x{height}). Maximum size is 4000x4000 pixels"
        
        # Check if image is corrupted by trying to convert
        image.convert('RGB')
        
        return True, "Image validation successful"
        
    except Exception as e:
        return False, f"Invalid or corrupted image: {str(e)}"

def validate_cow_image(image_bytes: bytes) -> tuple[bool, str]:
    """Use Gemini AI to validate if image contains a cow/cattle.
    
    Args:
        image_bytes: Raw bytes of the uploaded image
        
    Returns:
        Tuple of (is_cow, message)
    """
    gemini_client = get_gemini_client()
    
    if not gemini_client or not gemini_client.is_enabled():
        # If Gemini is not available, skip cow validation
        return True, "Cow validation skipped (AI not configured)"
    
    try:
        # Use Gemini Vision API to analyze the image
        is_cow, message = gemini_client.analyze_image_for_cow(image_bytes)
        return is_cow, message
        
    except Exception as e:
        print(f"⚠️ Cow validation error: {str(e)}")
        # On error, allow the image through (fail open)
        return True, f"Cow validation error (proceeding): {str(e)}"

# ======================================================================================
# GEMINI AI INTEGRATION ENDPOINTS
# ======================================================================================

@app.route('/gemini/status', methods=['GET'])
def gemini_status():
    """Check Gemini AI connection status."""
    try:
        status_result = test_gemini_connection()
        return jsonify(status_result), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error checking Gemini status: {str(e)}'
        }), 500

@app.route('/gemini/breed-insights/<breed_name>', methods=['GET'])
def get_gemini_breed_insights(breed_name):
    """Get enhanced breed insights using Gemini AI."""
    try:
        confidence = request.args.get('confidence', 0.8, type=float)
        gemini_client = get_gemini_client()
        
        if not gemini_client.is_enabled():
            return jsonify({
                'error': 'Gemini AI not configured',
                'message': 'Set GEMINI_API_KEY environment variable'
            }), 503
        
        insights = gemini_client.get_breed_insights(breed_name, confidence)
        return jsonify(insights), 200
        
    except Exception as e:
        return jsonify({'error': f'Error getting breed insights: {str(e)}'}), 500

@app.route('/gemini/farming-advice/<breed_name>', methods=['POST'])
def get_gemini_farming_advice(breed_name):
    """Get farming advice for a specific breed using Gemini AI."""
    try:
        data = request.get_json() or {}
        context = data.get('context', '')
        
        gemini_client = get_gemini_client()
        
        if not gemini_client.is_enabled():
            return jsonify({
                'error': 'Gemini AI not configured',
                'message': 'Set GEMINI_API_KEY environment variable'
            }), 503
        
        advice = gemini_client.get_farming_advice(breed_name, context)
        return jsonify(advice), 200
        
    except Exception as e:
        return jsonify({'error': f'Error getting farming advice: {str(e)}'}), 500

@app.route('/predict-enhanced', methods=['POST'])
def predict_enhanced():
    """Enhanced prediction with Gemini AI insights."""
    if MODEL is None:
        return jsonify({'error': 'Model not loaded'}), 503
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    try:
        file = request.files['image']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file. Please upload JPG, PNG, or WebP image.'}), 400
        
        # Get standard prediction
        start_time = time.time()
        image_bytes = file.read()
        image_tensor = transform_image(image_bytes)
        
        predicted_class, confidence, processing_time = get_prediction(image_tensor)
        
        # Get basic breed info
        breed_info_data = get_breed_info(predicted_class)
        
        # Get Gemini AI insights
        gemini_client = get_gemini_client()
        gemini_insights = {}
        
        if gemini_client.is_enabled():
            try:
                # Get breed insights
                insights = gemini_client.get_breed_insights(predicted_class, confidence)
                
                # Get contextual analysis
                prediction_results = {
                    'breed': predicted_class,
                    'confidence': confidence,
                    'processing_time': processing_time
                }
                analysis = gemini_client.analyze_prediction_context(prediction_results)
                
                gemini_insights = {
                    'breed_insights': insights,
                    'contextual_analysis': analysis,
                    'ai_enhanced': True
                }
            except Exception as e:
                gemini_insights = {
                    'error': f'Gemini AI error: {str(e)}',
                    'ai_enhanced': False
                }
        else:
            gemini_insights = {
                'message': 'Gemini AI not configured for enhanced insights',
                'ai_enhanced': False
            }
        
        total_time = time.time() - start_time
        
        response = {
            'prediction': predicted_class,
            'confidence': round(confidence, 4),
            'processing_time': round(processing_time, 3),
            'total_time': round(total_time, 3),
            'breed_info': breed_info_data,
            'gemini_insights': gemini_insights,
            'enhanced': True
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

# ======================================================================================
# 3. ERROR HANDLERS
# ======================================================================================

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 10MB.'}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

# ======================================================================================
# 4. STARTUP
# ======================================================================================


# ======================================================================================
# 4. INITIALIZATION
# ======================================================================================

# Attempt to load model at module level for WSGI servers (Gunicorn)
print("🔄 Initializing model during module import...")
try:
    load_model()
except Exception as e:
    print(f"⚠️  Warning: Model loading failed during import: {e}")
    print("    This is expected during build/CI. Model will be needed for predictions.")

if __name__ == '__main__':
    print("🚀 Starting Flask ML API Server...")
    
    # Check if model loaded successfully
    if MODEL is None:
        try:
            load_model()
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            print("⚠️  Server will start but predictions will not work until model is loaded.")
    else:
        print("✅ Model already loaded from module import.")
    
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 Server starting on http://0.0.0.0:{port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    )