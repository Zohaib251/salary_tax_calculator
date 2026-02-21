# api/index.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import traceback

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import tax calculations
try:
    from tax_calculations import calculate_advance_tax_logic
    print("✅ Successfully imported tax_calculations")
except Exception as e:
    print(f"❌ Error importing tax_calculations: {str(e)}")
    traceback.print_exc()
    calculate_advance_tax_logic = None

# Create Flask app
app = Flask(__name__, 
           static_folder='../', 
           static_url_path='',
           template_folder='../')

# Configure CORS
CORS(app, origins=['*'])

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return {}, 200

# Routes
@app.route('/')
def index():
    return send_from_directory('../', 'index.html')

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('../css', filename)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Tax Calculator API is running',
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

# Vercel handler
def handler(request, context):
    return app