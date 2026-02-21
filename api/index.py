# api/index.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Add parent directory to path so we can import tax_calculations
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import tax calculations
try:
    from tax_calculations import calculate_advance_tax_logic
    tax_module_loaded = True
except Exception as e:
    print(f"Error importing tax_calculations: {e}")
    tax_module_loaded = False
    calculate_advance_tax_logic = None

# Create Flask app
app = Flask(__name__, 
           static_folder='../static', 
           static_url_path='/static')

CORS(app)

@app.route('/')
def serve_frontend():
    return send_from_directory('..', 'index.html')

@app.route('/css/<path:path>')
def serve_css(path):
    return send_from_directory('../css', path)

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'tax_module': tax_module_loaded
    })

@app.route('/calculate-advance-tax', methods=['POST', 'OPTIONS'])
def calculate_tax():
    if request.method == 'OPTIONS':
        return '', 200
    
    if not tax_module_loaded:
        return jsonify({'error': 'Tax module not loaded'}), 500
    
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        result = calculate_advance_tax_logic(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# This is the Vercel handler
app.debug = False
handler = app