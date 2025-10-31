import json
import hashlib
import random
import time
from flask import Blueprint, jsonify, request
from datetime import datetime
import whois # Necessita di installazione: pip install python-whois

real_traffic_bp = Blueprint('real_traffic', __name__)

def get_domain_age_in_days(domain):
    """Tenta di ottenere l'età del dominio in giorni tramite WHOIS."""
    try:
        w = whois.whois(domain)
        if w.creation_date:
            # whois.whois può restituire una lista di date, prendiamo la prima
            if isinstance(w.creation_date, list):
                creation_date = w.creation_date[0]
            else:
                creation_date = w.creation_date
            
            # Calcola l'età in giorni
            if isinstance(creation_date, datetime):
                age = (datetime.now() - creation_date).days
                return max(1, age) # Assicura che l'età sia almeno 1 giorno
        return 365 # Default di 1 anno se la data di creazione non è disponibile
    except Exception:
        return 365 # Default di 1 anno in caso di errore WHOIS

def generate_traffic_data_v3(domain):
    """
    Algoritmo di Stima V3.0: Combina dati pubblici (Età Dominio) con hash coerente.
    """
    # 1. Dati Pubblici (Età del Dominio)
    domain_age_days = get_domain_age_in_days(domain)
    domain_age_years = domain_age_days / 365.0
    
    # 2. Hash Coerente (per la coerenza dei dati fittizi)
    domain_hash = int(hashlib.sha256(domain.encode('utf-8')).hexdigest(), 16)
    random.seed(domain_hash)

    # 3. Logica di Stima (Ponderazione)
    
    # Un dominio più vecchio ha un traffico di base più alto
    base_traffic_factor = 1 + (domain_age_years * random.uniform(0.1, 0.3))
    
    # Variazione casuale coerente per simulare l'autorità del dominio
    authority_score = random.uniform(0.5, 1.5)
    
    # Traffico di base (simulazione)
    base_traffic = random.randint(10000, 500000)
    
    # Stima del Traffico Unico
    visitors = int(base_traffic * base_traffic_factor * authority_score)
    visitors = max(100, visitors) # Minimo di 100 visitatori
    
    # Metriche Derivate
    pageviews = int(visitors * random.uniform(1.5, 3.0))
    bounce_rate = round(random.uniform(0.35, 0.75), 2)
    visit_duration = random.randint(60, 300) # Secondi
    
    # Dati di dettaglio (simulazione)
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
            "data_source": f"Algoritmo di Stima V3.0 (Età Dominio: {domain_age_years:.1f} anni)"
        }
    }

@real_traffic_bp.route('/analyze', methods=['POST'])
def analyze_traffic():
    """
    Endpoint per analizzare il traffico di un dominio (Algoritmo di Stima V3.0).
    """
    try:
        data = request.json
        domain = data.get('domain')

        if not domain:
            return jsonify({'error': 'Dominio non fornito.'}), 400

        # Rimuove http/https e www per standardizzare il dominio
        domain = domain.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]

        # Simula un piccolo ritardo per l'effetto "API call"
        time.sleep(random.uniform(0.5, 1.5))

        traffic_data = generate_traffic_data_v3(domain)
        
        return jsonify(traffic_data), 200

    except Exception as e:
        return jsonify({'error': f'Errore nell\'algoritmo di stima: {str(e)}'}), 500

@real_traffic_bp.route('/health', methods=['GET'])
def health_check():
    """Health check per l'API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '4.0.0 (Algoritmo di Stima V3.0)'
    })
