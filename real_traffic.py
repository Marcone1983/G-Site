from flask import Blueprint, jsonify, request, current_app
import requests
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse
import os

real_traffic_bp = Blueprint('real_traffic', __name__)

@real_traffic_bp.route('/proxy/plausible', methods=['POST'])
def proxy_plausible_query():
    """
    Endpoint proxy per inoltrare query all'API Plausible Stats.
    """
    plausible_api_key = current_app.config.get('PLAUSIBLE_API_KEY')
    plausible_api_url = current_app.config.get('PLAUSIBLE_API_URL')
    
    if not plausible_api_key or not plausible_api_url:
        return jsonify({
            'error': 'API Key o URL Plausible non configurati sul server.'
        }), 500

    try:
        # La query Plausible è nel corpo della richiesta POST
        query_data = request.json
        
        # Esegui la richiesta all'API Plausible
        headers = {
            'Authorization': f'Bearer {plausible_api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            plausible_api_url,
            headers=headers,
            json=query_data,
            timeout=30
        )
        
        # Inoltra la risposta di Plausible al client
        if response.ok:
            return jsonify(response.json()), response.status_code
        else:
            # Inoltra l'errore di Plausible al client
            return jsonify({
                'error': 'Errore dall\'API Plausible',
                'details': response.text
            }), response.status_code

    except Exception as e:
        return jsonify({'error': f'Errore nel proxy Plausible: {str(e)}'}), 500

@real_traffic_bp.route('/health', methods=['GET'])
def health_check():
    """Health check per l'API"""
    plausible_api_key = current_app.config.get('PLAUSIBLE_API_KEY')
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'plausible_api_configured': bool(plausible_api_key),
        'version': '2.0.0'
    })
