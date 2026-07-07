from flask import Blueprint, jsonify
from ..services.api_planilhas import selecionar_valor_celula
from datetime import datetime, timezone
import time

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/v1/status', methods=['GET'])
def status():
    nome = selecionar_valor_celula("Status", "A2")
    inicio_conexao = time.time()
    
    try:
        fim_conexao = time.time()
        latencia_ms = round(
            (fim_conexao - inicio_conexao) * 1000, 2
        )
        
        return jsonify({
            "Status": "Online",
            "Planilha": str(nome),
            "Connection": {
                "latencia_ms": latencia_ms,
                "time_connection": datetime.now(timezone.utc).isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "Status": "Offline",
            "Error": str(e),
            "Connection": {
                "time_connection": datetime.now(timezone.utc).isoformat()
            }
            
        }), 503
