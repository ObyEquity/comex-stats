import streamlit as st
import requests
import urllib3
import json

# Configuração SSL
BASE_URL = "https://api-comexstat.mdic.gov.br"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="Debug ComexStat", layout="wide")
st.title("🐞 Debug API ComexStat - Exportações por Município")

# Inputs do usuário
city_id = st.text_input("Digite o código IBGE do município:", "4208906")
from_period = st.text_input("Período inicial (AAAA-MM):", "2024-01")
to_period = st.text_input("Período final (AAAA-MM):", "2024-12")
month_detail = st.checkbox("Detalhar por mês?", value=True)

# Botão para depurar
if st.button("Depurar API"):
    url = f"{BASE_URL}/cities"
    payload = {
        "flow": "export",
        "monthDetail": month_detail,
        "period": {"from": from_period, "to": to_period},
        "filters": [{"filter": "city", "values": [int(city_id)]}],
        "details": ["country", "state", "city"],
        "metrics": ["metricFOB", "metricKG"]
    }

    try:
        response = requests.post(url, json=payload, verify=False)
        st.write("**Status Code:**", response.status_code)
        response.raise_for_status()
        data = response.json()
        
        # Mostrando tipo e keys
        st.write("**Tipo de retorno:**", type(data))
        if isinstance(data, dict):
            st.write("**Keys do JSON:**", list(data.keys()))
        
        # Mostrando exemplo de conteúdo
        if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
            st.write("**Exemplo de item do retorno:**")
            st.json(data["data"][0])
        else:
            st.warning("Nenhum dado encontrado no campo 'data'.")
            
    except requests.exceptions.RequestException as e:
        st.error(f"Erro na requisição: {e}")
