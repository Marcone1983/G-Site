import json
import hashlib
import random
from flask import Blueprint, jsonify, request
from datetime import datetime

real_traffic_bp = Blueprint('real_traffic', __name__)

def generate_traffic_data(domain):
    """
    Genera dati di traffico fittizi ma coerenti basati sull'hash del dominio.
    Simula l'API di SimilarWeb (V2.0).
    """
    # Usa un hash del dominio per garantire che lo stesso dominio
    # restituisca sempre gli stessi dati fittizi.
    domain_hash = int(hashlib.sha256(domain.encode('utf-8')).hexdigest(), 16)
    random.seed(domain_hash)

    # Logica di generazione dati
    
    # 1. Traffico di base (milioni)
    base_traffic = random.randint(100000, 5000000)
    
    # 2. Variazioni basate sulla lunghezza del nome (simula popolarità)
    if len(domain) < 10:
        base_traffic *= 1.5
    elif len(domain) > 20:
        base_traffic *= 0.5
        
    # 3. Aggiusta per un valore finale realistico
    visitors = int(base_traffic)
    pageviews = int(visitors * random.uniform(1.5, 3.0))
    
    # 4. Metriche aggiuntive
    bounce_rate = round(random.uniform(0.35, 0.75), 2)
    visit_duration = random.randint(60, 300) # Secondi
    
    # 5. Dati di dettaglio (simulazione)
    traffic_sources = [
        {"channel": "Direct", "value": int(visitors * random.uniform(0.2, 0.3))},
        {"channel": "Search", "value": int(visitors * random.uniform(0.3, 0.4))},
        {"channel": "Social", "value": int(visitors * random.uniform(0.05, 0.15))},
        {"channel": "Referral", "value": int(visitors * random.uniform(0.05, 0.15))},
        {"channel": "Mail", "value": int(visitors * random.uniform(0.01, 0.05))},
    ]
    
    # Normalizza i totali per evitare discrepanze
    total_sources = sum(item['value'] for item in traffic_sources)
    if total_sources > visitors:
        # Se il totale è maggiore, scala per non superare il totale visitatori
        scale_factor = visitors / total_sources
        for item in traffic_sources:
            item['value'] = int(item['value'] * scale_factor)

    return {
        "domain": domain,
        "metrics": {
            "visitors": {"value": visitors, "unit": "count"},
            "pageviews": {"value": pageviews, "unit": "count"},
            "bounce_rate": {"value": bounce_rate, "unit": "ratio"},
            "visit_duration": {"value": visit_duration, "unit": "seconds"},
        },
        "details": {
            "traffic_sources": traffic_sources,
            "data_source": "SimilarWeb V2.0 (Simulazione)"
        }
    }

@real_traffic_bp.route('/analyze', methods=['POST'])
def analyze_traffic():
    """
    Endpoint per analizzare il traffico di un dominio (Simulazione SimilarWeb).
    """
    try:
        data = request.json
        domain = data.get('domain')

        if not domain:
            return jsonify({'error': 'Dominio non fornito.'}), 400

        # Rimuove http/https e www per standardizzare il dominio
        domain = domain.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]

        # Simula un piccolo ritardo per l'effetto "API call"
        # time.sleep(random.uniform(0.5, 1.5))

        traffic_data = generate_traffic_data(domain)
        
        return jsonify(traffic_data), 200

    except Exception as e:
        return jsonify({'error': f'Errore nel simulatore API: {str(e)}'}), 500

@real_traffic_bp.route('/health', methods=['GET'])
def health_check():
    """Health check per l'API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '3.0.0 (Simulated SimilarWeb)'
    })
