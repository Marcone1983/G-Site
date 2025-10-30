import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from real_traffic import real_traffic_bp
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configurazione Plausible
PLAUSIBLE_API_KEY = os.environ.get('PLAUSIBLE_API_KEY')
PLAUSIBLE_API_URL = os.environ.get('PLAUSIBLE_API_URL', 'https://plausible.io/api/v2/query')

app = Flask(__name__, static_folder='build', static_url_path='/build', template_folder=os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
app.config['PLAUSIBLE_API_KEY'] = PLAUSIBLE_API_KEY
app.config['PLAUSIBLE_API_URL'] = PLAUSIBLE_API_URL
CORS(app)

app.register_blueprint(real_traffic_bp, url_prefix='/api/traffic')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Gestione file statici per Vite
    if path.endswith(('.js', '.jsx', '.css')):
        return send_from_directory(app.template_folder, path)
    
    # Gestione della SPA (Single Page Application)
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    # Endpoint per esporre la configurazione del backend al frontend
    return jsonify({
        'plausible_api_url': PLAUSIBLE_API_URL,
        'plausible_api_key_configured': bool(PLAUSIBLE_API_KEY)
    })

if __name__ == '__main__':
    app.run(debug=True)
