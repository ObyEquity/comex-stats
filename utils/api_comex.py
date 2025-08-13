import requests
import pandas as pd
import urllib3

BASE_URL = "https://api-comexstat.mdic.gov.br/cities"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

def get_cities_by_state(state_code=None, period_from="2018-01", period_to="2018-01", flow="export"):
    """
    Retorna lista de cidades disponíveis.
    Se state_code for None, retorna todas as cidades (dependendo da API).
    """
    filters = []
    if state_code:
        filters.append({"filter": "state", "values": [state_code]})
    
    payload = {
        "flow": flow,
        "monthDetail": False,
        "period": {"from": period_from, "to": period_to},
        "filters": filters,
        "details": ["city", "state"],
        "metrics": ["metricFOB"]
    }
    
    r = requests.post(BASE_URL, json=payload, headers=HEADERS, verify=False)
    r.raise_for_status()
    data = r.json()
    
    if "data" in data and isinstance(data["data"], dict) and "list" in data["data"]:
        df = pd.DataFrame(data["data"]["list"])
        if "city" in df.columns:
            return df.drop_duplicates(subset=["city"]).sort_values("city")
    return pd.DataFrame()

def get_exports_by_city(city_name, state_code, flow="export", period_from="2018-01", period_to="2018-12"):
    """
    Consulta exportações/importações de uma cidade específica.
    """
    payload = {
        "flow": flow,
        "monthDetail": False,
        "period": {"from": period_from, "to": period_to},
        "filters": [{"filter": "state", "values": [state_code]}],
        "details": ["country", "state", "city"],
        "metrics": ["metricFOB", "metricKG"]
    }
    
    r = requests.post(BASE_URL, json=payload, headers=HEADERS, verify=False)
    r.raise_for_status()
    data = r.json()
    
    if "data" in data and isinstance(data["data"], dict) and "list" in data["data"]:
        df = pd.DataFrame(data["data"]["list"])
        return df[df["city"] == city_name] if "city" in df.columns else pd.DataFrame()
    return pd.DataFrame()
