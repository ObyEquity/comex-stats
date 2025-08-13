import streamlit as st
import requests
import urllib3

# Desabilitar warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://api-comexstat.mdic.gov.br/cities"

st.set_page_config(page_title="Debug ComexStat - Município", layout="wide")
st.title("🐞 Debug API ComexStat - Exportação/Importação por Município")

st.markdown(
    """
Este app envia o payload oficial da API ComexStat, incluindo headers de navegador,
e mostra a resposta de forma segura considerando a nova estrutura do JSON.
"""
)

# Inputs do usuário
flow = st.selectbox("Fluxo:", ["export", "import"])
state = st.text_input("Código do estado (UF):", "26")  # obrigatório
from_period = st.text_input("Período inicial (AAAA-MM):", "2018-01")
to_period = st.text_input("Período final (AAAA-MM):", "2018-01")
month_detail = st.checkbox("Detalhar por mês?", value=False)

details = st.multiselect(
    "Detalhes desejados:",
    ["country", "state", "city", "ncm"],
    default=["country", "state"]
)

metrics = st.multiselect(
    "Métricas desejadas:",
    ["metricFOB", "metricKG", "metricStatistic", "metricFreight", "metricInsurance", "metricCIF"],
    default=["metricFOB", "metricKG"]
)

# Botão para depurar
if st.button("Enviar requisição"):
    # Construir payload
    payload = {
        "flow": flow,
        "monthDetail": month_detail,
        "period": {"from": from_period, "to": to_period},
        "filters": [{"filter": "state", "values": [int(state)]}],
        "details": details,
        "metrics": metrics
    }

    st.subheader("Payload enviado:")
    st.json(payload)

    # Headers simulando navegador
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=headers, verify=False)
        st.write("**Status Code:**", response.status_code)
        st.subheader("Resposta bruta (texto, primeiros 1000 caracteres):")
        st.text(response.text[:1000])

        response.raise_for_status()
        data = response.json()

        st.subheader("Keys do JSON retornado:")
        st.write(list(data.keys()))

        # Novo acesso considerando data["list"]
        if "data" in data and isinstance(data["data"], dict) and "list" in data["data"]:
            if len(data["data"]["list"]) > 0:
                st.subheader("Exemplo de item retornado:")
                st.json(data["data"]["list"][0])
            else:
                st.warning("A lista 'data[list]' está vazia.")
        else:
            st.warning("Nenhum dado encontrado no campo 'data'.")

    except requests.exceptions.RequestException as e:
        st.error(f"Erro na requisição: {e}")
