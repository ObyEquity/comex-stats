import requests
import urllib3
import json

BASE_URL = "https://api-comexstat.mdic.gov.br"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def debug_city_exports(city_id, from_period="2024-01", to_period="2024-12"):
    """
    Função para depurar retorno da API de exportações por município.
    Exibe JSON bruto e keys principais.
    """
    url = f"{BASE_URL}/cities"
    
    payload = {
        "flow": "export",
        "monthDetail": True,
        "period": {"from": from_period, "to": to_period},
        "filters": [{"filter": "city", "values": [city_id]}],
        "details": ["country", "state", "city"],
        "metrics": ["metricFOB", "metricKG"]
    }
    
    try:
        response = requests.post(url, json=payload, verify=False)
        print("Status Code:", response.status_code)
        response.raise_for_status()
        
        data = response.json()
        print("Tipo de retorno:", type(data))
        print("Keys do JSON:", data.keys() if isinstance(data, dict) else "Não é dict")
        print("Exemplo de conteúdo (1 item):", json.dumps(data.get("data", data)[:1], indent=2) if "data" in data else data)
        
        return data
    
    except requests.exceptions.RequestException as e:
        print("Erro na requisição:", e)
        return None
