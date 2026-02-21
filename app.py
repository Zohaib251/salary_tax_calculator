# app.py - Main Flask app for Vercel
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from tax_calculations import calculate_advance_tax_logic

# Create Flask app FIRST
app = Flask(__name__, 
           static_folder='.', 
           static_url_path='',
           template_folder='.')

# Configure CORS for production
CORS(app, origins=['*'])  # You can restrict this to your domain later

# THEN add the before_request handler (after app is created)
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        return response

# Create necessary folders (Vercel will have read-only filesystem)
# Remove the folder creation code as Vercel filesystem is read-only
# The folders should already exist in your repository

# --- Routes ---
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

@app.route('/calculate-advance-tax', methods=['POST', 'OPTIONS'])
def calculate_advance_tax():
    # Handle OPTIONS request for CORS
    if request.method == "OPTIONS":
        return {}, 200
        
    try:
        # Handle both form data and JSON
        if request.is_json:
            form_data = request.get_json()
        else:
            form_data = request.form.to_dict()
        
        response = calculate_advance_tax_logic(form_data)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Health check endpoint (useful for Vercel)
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Tax Calculator API is running'})

# This is for local development only
if __name__ == '__main__':
    print("\n" + "="*60)
    print("💰 TAX CALCULATOR SERVER")
    print("="*60)
    print(f"\n🔗 Local URL: http://localhost:5000")
    print("="*60)
    print("\nPress Ctrl+C to stop the server")
    print("="*60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )