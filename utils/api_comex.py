import requests
import pandas as pd

BASE_URL = "https://api-comexstat.mdic.gov.br"

def get_cities():
    """Retorna lista de cidades disponíveis na API do Comex Stat."""
    url = f"{BASE_URL}/cities/"
    r = requests.get(url)
    r.raise_for_status()
    return pd.DataFrame(r.json())

def get_exports_by_city(city_id, year=None):
    """Consulta exportações de uma cidade específica."""
    url = f"{BASE_URL}/exports/cities/{city_id}/"
    params = {}
    if year:
        params["year"] = year
    r = requests.get(url, params=params)
    r.raise_for_status()
    return pd.DataFrame(r.json())
