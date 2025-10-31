import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from real_traffic import real_traffic_bp

app = Flask(__name__, static_folder='build', static_url_path='/build', template_folder=os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

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

if __name__ == '__main__':
    app.run(debug=True)
