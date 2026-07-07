import requests
from datetime import datetime
from app.routes.api import status

def test_api_v1_status_deve_retornar_200():
    response = requests.get("http://127.0.0.1:5000/api/v1/status")
    
    # O assert equivale ao "expect - ToBe" dos testes de JavaScript
    assert response.status_code == 200
    
def test_propriedade_status_deve_ser_online_ou_offline():
    response = requests.get("http://127.0.0.1:5000/api/v1/status")
    responseBody = response.json()
    
    assert "Status" in responseBody
    
    assert responseBody["Status"] == "Online" or responseBody["Status"] == "Offline"
    

def test_propriedade_planilha_deve_ser_dev_ou_prod():
    response = requests.get("http://127.0.0.1:5000/api/v1/status")
    responseBody = response.json()
    
    assert "Planilha" in responseBody
    
    assert responseBody["Planilha"] == "Development" or responseBody["Planilha"] == "Production"

def test_propriedade_time_connection_deve_ser_a_data_atual():
    response = requests.get("http://127.0.0.1:5000/api/v1/status")
    responseBody = response.json()
    
    # Testa se o valor existe (equivalente ao toBeDefined em JavaScript)
    assert "Connection" in responseBody
    assert "time_connection" in responseBody["Connection"]
    assert responseBody["Connection"]["time_connection"] is not None
    
    time_connection_str = responseBody["Connection"]["time_connection"]
    try:
        datetime.fromisoformat(time_connection_str)
        is_valid_iso = True
    except ValueError:
        is_valid_iso = False
    
    assert is_valid_iso is True
