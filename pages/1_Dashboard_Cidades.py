import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_comex import get_cities, get_exports_by_city

st.set_page_config(page_title="Dashboard por Cidade", layout="wide")

st.title("🏙️ Exportações por Cidade - Comex Stat")

# Seleção de cidade
cities_df = get_cities()
city_name = st.selectbox("Selecione a cidade:", cities_df["name"].unique())

city_id = cities_df.loc[cities_df["name"] == city_name, "id"].values[0]

# Seleção de ano
year = st.selectbox("Ano:", list(range(2015, 2025)))

# Buscar dados
st.info("Buscando dados da API...")
data_df = get_exports_by_city(city_id, year)

if not data_df.empty:
    st.subheader(f"Exportações de {city_name} em {year}")
    fig = px.bar(
        data_df,
        x="produto",
        y="valor",
        title=f"Exportações por produto - {city_name} ({year})",
        labels={"produto": "Produto", "valor": "Valor (US$)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(data_df)
else:
    st.warning("Nenhum dado encontrado para esta cidade e ano.")
