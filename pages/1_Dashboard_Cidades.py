import streamlit as st
import pandas as pd
from utils.api_comex import get_exports_imports

st.set_page_config(page_title="Dashboard Cidades - ComexStat", layout="wide")
st.title("📊 Dashboard de Exportações/Importações por Município")

# ---- FILTROS ----
st.sidebar.header("Filtros")

flow = st.sidebar.radio("Fluxo:", ["export", "import"])
period_from = st.sidebar.text_input("Período inicial (AAAA-MM):", "2018-01")
period_to = st.sidebar.text_input("Período final (AAAA-MM):", "2018-12")

# Lista completa de estados
estados = {
    "AC": 12, "AL": 27, "AP": 16, "AM": 13, "BA": 29, "CE": 23,
    "DF": 53, "ES": 32, "GO": 52, "MA": 21, "MT": 51, "MS": 50,
    "MG": 31, "PA": 15, "PB": 25, "PR": 41, "PE": 26, "PI": 22,
    "RJ": 33, "RN": 24, "RS": 43, "RO": 11, "RR": 14, "SC": 42,
    "SP": 35, "SE": 28, "TO": 17
}

state_name = st.sidebar.selectbox("Estado:", list(estados.keys()))
state_code = estados[state_name]

# ---- Obter dados do estado ----
with st.spinner("Carregando dados do estado..."):
    df_state = get_exports_imports(state_code, flow, period_from, period_to)

if df_state.empty:
    st.warning("Nenhum dado encontrado para o estado e período selecionados.")
else:
    # Filtrar cidades disponíveis
    cities = sorted(df_state["city"].dropna().unique())
    city_name = st.sidebar.selectbox("Cidade:", cities)

    # Filtrar dados da cidade
    df_city = df_state[df_state["city"] == city_name]

    st.subheader(f"Dados de {city_name} ({flow})")
    st.dataframe(df_city)

    # Gráfico por país
    chart_data = (
        df_city.groupby("country")[["metricFOB", "metricKG"]]
        .sum()
        .sort_values("metricFOB", ascending=False)
    )
    st.subheader("Resumo por país")
    st.bar_chart(chart_data)
