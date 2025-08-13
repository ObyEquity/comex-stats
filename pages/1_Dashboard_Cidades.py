import streamlit as st
import pandas as pd
from utils.api_comex import get_cities_by_state, get_exports_by_city

st.set_page_config(page_title="Dashboard Cidades - ComexStat", layout="wide")
st.title("📊 Dashboard de Exportações/Importações por Município")

# ---- FILTROS ----
st.sidebar.header("Filtros")

flow = st.sidebar.radio("Fluxo:", ["export", "import"])
period_from = st.sidebar.text_input("Período inicial (AAAA-MM):", "2018-01")
period_to = st.sidebar.text_input("Período final (AAAA-MM):", "2018-12")

# Estados: manualmente ou buscar uma lista de UF disponíveis
estados = {
    "SP": 35,
    "RJ": 33,
    "MG": 31,
    "RS": 43,
    "SC": 42,
    # adicionar outros estados conforme necessidade
}
state_name = st.sidebar.selectbox("Estado:", list(estados.keys()))
state_code = estados[state_name]

# Cidades dependentes do estado selecionado
with st.spinner("Carregando cidades..."):
    cities_df = get_cities_by_state(state_code, period_from=period_from, period_to=period_to, flow=flow)

if cities_df.empty:
    st.warning("Nenhuma cidade encontrada para o estado selecionado.")
else:
    city_name = st.sidebar.selectbox("Cidade:", sorted(cities_df["city"].unique()))

    if st.sidebar.button("Buscar dados"):
        with st.spinner(f"Consultando dados da cidade {city_name}..."):
            df_city = get_exports_by_city(city_name, state_code, flow, period_from, period_to)
            
            if df_city.empty:
                st.warning("Nenhum dado encontrado para os filtros selecionados.")
            else:
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
