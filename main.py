import os
import sys


from flask import Flask, send_from_directory
from flask_cors import CORS
from user import db
from user import user_bp
from real_traffic import real_traffic_bp

# Configurazione Flask per servire i file statici dalla cartella 'build'
# e l'index.html dalla root del progetto.
# La cartella 'build' contiene gli asset statici (JS, CSS, ecc.)
# La cartella 'static' è impostata su 'build'
# La cartella 'template' è impostata sulla root del progetto dove si trova index.html
app = Flask(__name__, static_folder='build', template_folder=os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Abilita CORS per tutte le route
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(real_traffic_bp, url_prefix='/api/traffic')

# uncomment if you need to use database
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# with app.app_context():
#     db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Se il percorso è per un file statico all'interno di 'build' (es. /build/index.js)
    # Flask lo serve automaticamente grazie a static_folder='build'.
    
    # Se il percorso è per un file statico nella root (es. /index.html, /app.css)
    # o per il routing della SPA, serviamo index.html
    
    # Tentativo di servire il file statico dalla cartella 'build'
    if path != "":
        # Controlla se il file esiste nella cartella 'build'
        static_file_path = os.path.join(app.static_folder, path)
        if os.path.exists(static_file_path):
            return send_from_directory(app.static_folder, path)
        
        # Controlla se il file esiste nella root (es. app.css, index.js)
        # Questo è necessario perché il frontend potrebbe fare riferimento a file nella root
        root_file_path = os.path.join(app.template_folder, path)
        if os.path.exists(root_file_path):
            return send_from_directory(app.template_folder, path)

    # Per tutte le altre rotte (inclusa la root '/') e per i percorsi SPA, servi index.html
    return send_from_directory(app.template_folder, 'index.html')


# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000, debug=True)
