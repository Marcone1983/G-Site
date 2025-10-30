import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from user import user_bp
from real_traffic import real_traffic_bp

app = Flask(__name__, static_folder='build', static_url_path='/build', template_folder=os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(real_traffic_bp, url_prefix='/api/traffic')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    return send_from_directory(app.template_folder, 'index.html')
