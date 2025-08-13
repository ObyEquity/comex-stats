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

def get_exports_imports(state_code, flow="export", period_from="2018-01", period_to="2018-12"):
    """
    Consulta exportações/importações de um estado e retorna DataFrame completo.
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
        return df
    return pd.DataFrame()
