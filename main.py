import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from real_traffic import real_traffic_bp

app = Flask(__name__, static_folder='build', static_url_path='/', template_folder=os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

CORS(app)

app.register_blueprint(real_traffic_bp, url_prefix='/api/traffic')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Gestione della SPA (Single Page Application)
    # Se il path è un file statico (es. main.js, index.css) lo cerchiamo nella cartella 'build'
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    
    # Altrimenti, serviamo l'index.html dalla cartella 'build'
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
