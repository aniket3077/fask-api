"""
Simple Flask API for testing backend integration
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Flask API is running',
        'service': 'flask-ml-api'
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Mock prediction endpoint for testing"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    # Mock prediction response
    mock_prediction = {
        'breed': 'Holstein',
        'confidence': 0.95,
        'message': 'Mock prediction - ML model will be loaded here'
    }
    
    return jsonify(mock_prediction)

@app.route('/breeds', methods=['GET'])
def get_breeds():
    """Get available cattle breeds"""
    breeds = [
        'Holstein', 'Jersey', 'Angus', 'Hereford', 'Charolais',
        'Simmental', 'Limousin', 'Brahman', 'Brown Swiss', 'Gelbvieh'
    ]
    return jsonify({'breeds': breeds})

if __name__ == '__main__':
    print("🚀 Starting Simple Flask API Server...")
    print("🌐 Server starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)