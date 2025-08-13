import streamlit as st
from utils.api_comex import get_cities, get_exports_by_city

st.set_page_config(page_title="Dashboard por Cidade", layout="wide")
st.title("🏙️ Exportações por Cidade")

# Carregar cidades
cities_df = get_cities()

# Seleção de cidade
city_name = st.selectbox("Selecione a cidade:", cities_df["city"].unique())
city_id = int(cities_df.loc[cities_df["city"] == city_name, "cityId"].values[0])

# Seleção de período
from_period = st.text_input("Período inicial (AAAA-MM):", "2024-01")
to_period = st.text_input("Período final (AAAA-MM):", "2024-12")

# Buscar dados
st.info("Buscando dados da API...")
df_exports = get_exports_by_city(city_id, from_period=from_period, to_period=to_period)

if not df_exports.empty:
    st.subheader(f"Exportações de {city_name} ({from_period} → {to_period})")
    st.dataframe(df_exports)
else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
