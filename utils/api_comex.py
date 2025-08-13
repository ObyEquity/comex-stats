import requests
import urllib3
import pandas as pd

BASE_URL = "https://api-comexstat.mdic.gov.br/cities"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_cities():
    """Retorna lista de cidades disponíveis na API do Comex Stat."""
    payload = {
        "flow": "export",
        "monthDetail": False,
        "period": {"from": "2018-01", "to": "2018-01"},
        "filters": [],
        "details": ["city"],
        "metrics": ["metricFOB"]
    }
    r = requests.post(BASE_URL, json=payload, headers=HEADERS, verify=False)
    r.raise_for_status()
    data = r.json()
    # Checa se 'list' existe
    if "data" in data and isinstance(data["data"], dict) and "list" in data["data"]:
        return pd.DataFrame(data["data"]["list"])
    return pd.DataFrame()

def get_exports_by_city(city_name, state_code, flow="export", period_from="2018-01", period_to="2018-12"):
    """Consulta exportações/importações de uma cidade específica."""
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
        if "city" in df.columns:
            return df[df["city"] == city_name]
    return pd.DataFrame()
