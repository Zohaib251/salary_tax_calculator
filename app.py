# app.py - Main Flask app for Vercel
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import traceback

print("="*50)
print("Starting app.py")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")
print("="*50)

# Check if tax_calculations.py exists
if os.path.exists('tax_calculations.py'):
    print("✅ tax_calculations.py found")
else:
    print("❌ tax_calculations.py NOT found")
    print(f"Looking for .py files: {[f for f in os.listdir('.') if f.endswith('.py')]}")

try:
    from tax_calculations import calculate_advance_tax_logic
    print("✅ Successfully imported calculate_advance_tax_logic")
except Exception as e:
    print("❌ Error importing tax_calculations:")
    print(str(e))
    print(traceback.format_exc())
    # Don't raise here, let the app try to start
    calculate_advance_tax_logic = None

# Create Flask app FIRST
app = Flask(__name__, 
           static_folder='.', 
           static_url_path='',
           template_folder='.')

# Configure CORS
CORS(app, origins=['*'])

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        return response

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

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Tax Calculator API is running',
        'files': os.listdir('.'),
        'tax_calculations_loaded': calculate_advance_tax_logic is not None
    })

@app.route('/calculate-advance-tax', methods=['POST', 'OPTIONS'])
def calculate_advance_tax():
    if request.method == "OPTIONS":
        return {}, 200
    
    if calculate_advance_tax_logic is None:
        return jsonify({'error': 'Tax calculation module not loaded'}), 500
        
    try:
        if request.is_json:
            form_data = request.get_json()
        else:
            form_data = request.form.to_dict()
        
        response = calculate_advance_tax_logic(form_data)
        return jsonify(response)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'API is working!'})

# This is for local development only
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)