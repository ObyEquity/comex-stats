import requests
import pandas as pd
import urllib3

# Base da API ComexStat
BASE_URL = "https://api-comexstat.mdic.gov.br"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_cities():
    """
    Retorna a lista de cidades disponíveis na API do Comex Stat.
    Como a API exige POST, fazemos uma requisição mínima.
    """
    url = f"{BASE_URL}/cities"
    
    payload = {
        "flow": "export",            # ou "import", apenas para listar cidades
        "monthDetail": False,
        "period": {"from": "2024-01", "to": "2024-01"},  # período dummy
        "filters": [],               # sem filtros retorna todas
        "details": ["state", "city"],
        "metrics": ["metricFOB"]
    }

    r = requests.post(url, json=payload, verify=False)
    r.raise_for_status()
    data = r.json()
    
    # Retorna DataFrame somente com a lista de cidades
    if "data" in data:
        return pd.DataFrame(data["data"])
    else:
        return pd.DataFrame()

def get_exports_by_city(city_id, from_period="2024-01", to_period="2024-12", flow="export", month_detail=True, details=None, metrics=None):
    """
    Consulta exportações ou importações de uma cidade específica.
    
    Parâmetros:
        city_id (int): Código IBGE da cidade.
        from_period (str): Data inicial no formato "AAAA-MM".
        to_period (str): Data final no formato "AAAA-MM".
        flow (str): "export" ou "import".
        month_detail (bool): Se True, retorna detalhamento mensal.
        details (list): Lista de detalhes, ex: ["country", "state", "ncm"].
        metrics (list): Lista de métricas, ex: ["metricFOB", "metricKG"].
    """
    url = f"{BASE_URL}/cities"
    
    if details is None:
        details = ["country", "state"]
    if metrics is None:
        metrics = ["metricFOB", "metricKG"]
    
    payload = {
        "flow": flow,
        "monthDetail": month_detail,
        "period": {"from": from_period, "to": to_period},
        "filters": [{"filter": "city", "values": [city_id]}],
        "details": details,
        "metrics": metrics
    }
    
    r = requests.post(url, json=payload, verify=False)
    r.raise_for_status()
    data = r.json()
    
    if "data" in data:
        return pd.DataFrame(data["data"])
    else:
        return pd.DataFrame()
