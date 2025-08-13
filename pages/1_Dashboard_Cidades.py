import streamlit as st
import pandas as pd
from utils.api_comex import get_cities, get_exports_by_city

st.set_page_config(page_title="Dashboard Cidades - ComexStat", layout="wide")
st.title("📊 Dashboard de Exportações/Importações por Município")
st.markdown("Visualize dados por cidade usando a API ComexStat.")

# Carregar cidades
with st.spinner("Carregando cidades..."):
    cities_df = get_cities()

if cities_df.empty:
    st.warning("Não foi possível carregar cidades da API.")
else:
    st.subheader("Debug: colunas do DataFrame de cidades")
    st.write(cities_df.columns)
    st.dataframe(cities_df.head())

    # Detecta coluna de cidade
    city_col = "city" if "city" in cities_df.columns else cities_df.columns[0]

    st.subheader("Selecione filtros")
    city_name = st.selectbox("Cidade:", sorted(cities_df[city_col].unique()))
    state_code = st.text_input("Código do estado (UF):", value="26")
    flow = st.radio("Fluxo:", ["export", "import"])
    period_from = st.text_input("Período inicial (AAAA-MM):", value="2018-01")
    period_to = st.text_input("Período final (AAAA-MM):", value="2018-12")

    if st.button("Buscar dados"):
        with st.spinner("Consultando dados da cidade..."):
            df_city = get_exports_by_city(city_name, int(state_code), flow, period_from, period_to)

            if df_city.empty:
                st.warning("Nenhum dado encontrado para os filtros selecionados.")
            else:
                st.subheader(f"Dados da cidade: {city_name} ({flow})")
                st.dataframe(df_city)

                # Gráfico de exportações/importações por país
                st.subheader("Gráfico por país")
                chart_data = (
                    df_city.groupby("country")[["metricFOB", "metricKG"]]
                    .sum()
                    .sort_values("metricFOB", ascending=False)
                )
                st.bar_chart(chart_data)
