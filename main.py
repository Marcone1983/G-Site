import os
import sys


from flask import Flask, send_from_directory
from flask_cors import CORS
from user import db
from user import user_bp
from real_traffic import real_traffic_bp

app = Flask(__name__, static_folder='build', static_url_path='/', template_folder=os.path.dirname(__file__))
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
    if path == "":
        return send_from_directory(app.template_folder, 'index.html')
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    # Se il percorso corrisponde a un file statico esistente, servilo
    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    
    # Altrimenti, per tutte le altre rotte (SPA routing), servi sempre index.html
    return send_from_directory(app.template_folder, 'index.html')


# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000, debug=True)
