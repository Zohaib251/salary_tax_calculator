# app.py - Main Flask app with CLI arguments
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import argparse
from tax_calculations import calculate_advance_tax_logic

# Parse command line arguments
parser = argparse.ArgumentParser(description='Tax Calculator Server')
parser.add_argument('--public', action='store_true', help='Create public URL with ngrok')
parser.add_argument('--ngrok-token', type=str, help='Ngrok authtoken (optional)')
parser.add_argument('--port', type=int, default=5000, help='Port to run on (default: 5000)')
parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
parser.add_argument('--debug', action='store_true', help='Run in debug mode')

args = parser.parse_args()

# Create Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Create necessary folders
folders = ['css', 'js', 'images']
for folder in folders:
    os.makedirs(folder, exist_ok=True)

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

@app.route('/calculate-advance-tax', methods=['POST'])
def calculate_advance_tax():
    try:
        form_data = request.form.to_dict()
        response = calculate_advance_tax_logic(form_data)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("\n" + "="*60)
    print("💰 TAX CALCULATOR SERVER")
    print("="*60)
    
    public_url = None
    
    # Handle ngrok if --public flag is set
    if args.public:
        try:
            from pyngrok import ngrok
            
            # Get ngrok token
            token = args.ngrok_token
            if not token:
                print("\n🔑 Ngrok Setup Required:")
                print("-"*30)
                print("1. Get free token from: https://dashboard.ngrok.com")
                print("2. Sign up if you haven't")
                print("3. Get authtoken from dashboard")
                token = input("\nEnter your ngrok authtoken: ").strip()
            
            if token:
                ngrok.set_auth_token(token)
                public_url = ngrok.connect(args.port).public_url
                print(f"\n✅ PUBLIC URL CREATED!")
                print(f"🌍 {public_url}")
                
                # Create WhatsApp message
                whatsapp_msg = f"""*TAX CALCULATOR TEST* 🧮

Hey! Please test my salary tax calculator:

🔗 *Live URL:* {public_url}

*Features:*
✅ Automatic tax calculations
✅ Real-time updates
✅ Pakistan tax slabs
✅ Pension tax rules

*Quick Test:*
1. Enter any salary amount
2. Add some allowances
3. See tax calculated instantly

Let me know if it works! 🚀"""
                
                print("\n📱 WhatsApp message ready to share!")
                print("-"*40)
                print(whatsapp_msg)
                print("-"*40)
            else:
                print("\n⚠️  No ngrok token provided. Running locally only.")
                
        except ImportError:
            print("\n⚠️  pyngrok not installed. Install with: pip install pyngrok")
            print("Running locally only.")
        except Exception as e:
            print(f"\n⚠️  Ngrok error: {e}")
            print("Running locally only.")
    
    print(f"\n🔗 Local URL: http://localhost:{args.port}")
    if public_url:
        print(f"🌍 Public URL: {public_url}")
    print("="*60)
    print("\nPress Ctrl+C to stop the server")
    print("="*60)
    
    # Run Flask
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug or (not args.public)  # Debug mode unless public
    )