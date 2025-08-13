import streamlit as st
import requests
import urllib3

# Desabilitar warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://api-comexstat.mdic.gov.br/cities"

st.set_page_config(page_title="Teste Payload Oficial ComexStat", layout="wide")
st.title("💡 Teste Payload Oficial - ComexStat")

st.markdown("Este teste envia exatamente o payload oficial da documentação da API.")

# Payload oficial
payload_oficial = {
    "flow": "export",
    "monthDetail": False,
    "period": {
        "from": "2018-01",
        "to": "2018-01"
    },
    "filters": [
        {
            "filter": "state",
            "values": [26]
        }
    ],
    "details": ["country", "state"],
    "metrics": ["metricFOB", "metricKG"]
}

st.subheader("Payload enviado:")
st.json(payload_oficial)

if st.button("Enviar requisição"):
    try:
        response = requests.post(BASE_URL, json=payload_oficial, verify=False)
        st.write("**Status Code:**", response.status_code)
        response.raise_for_status()
        data = response.json()

        st.subheader("Keys do JSON retornado:")
        st.write(list(data.keys()))

        if "data" in data and data["data"]:
            st.subheader("Exemplo de item retornado:")
            st.json(data["data"][0])
        else:
            st.warning("Nenhum dado encontrado no campo 'data'.")
            
    except requests.exceptions.RequestException as e:
        st.error(f"Erro na requisição: {e}")
