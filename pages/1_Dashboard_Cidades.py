import streamlit as st
import pandas as pd
from utils.api_comex import get_exports_imports  # Certifique-se de ajustar a função se necessário

st.set_page_config(page_title="Dashboard Cidades - ComexStat", layout="wide")
st.title("📊 Dashboard de Exportações/Importações por Município")

# ---- FILTROS ----
st.sidebar.header("Filtros")
flow = st.sidebar.radio("Fluxo:", ["export", "import"])
period_from = st.sidebar.text_input("Período inicial (AAAA-MM):", "2018-01")
period_to = st.sidebar.text_input("Período final (AAAA-MM):", "2018-12")

# ---- Lista corrigida de estados ----
estados = {
    "AC": 12, "AL": 27, "AP": 16, "AM": 13, "BA": 32, "CE": 23,
    "DF": 54, "ES": 34, "GO": 53, "MA": 21, "MT": 52, "MS": 55,
    "MG": 33, "PA": 15, "PB": 25, "PR": 42, "PE": 26, "PI": 22,
    "RJ": 36, "RN": 24, "RS": 45, "RO": 11, "RR": 14, "SC": 44,
    "SP": 41, "SE": 31, "TO": 17
}

state_name = st.sidebar.selectbox("Estado:", list(estados.keys()))
state_code = estados[state_name]

# ---- Obter dados do estado ----
with st.spinner(f"Carregando dados de {state_name}..."):
    df_state = get_exports_imports(state_code, flow, period_from, period_to)

# ---- DEBUG: mostrar informações do DataFrame ----
st.subheader("Debug: Dados brutos do DataFrame")
st.write("Número de linhas:", len(df_state))
st.write("Colunas disponíveis:", df_state.columns.tolist())
st.dataframe(df_state.head(10))

if df_state.empty:
    st.warning("Nenhum dado encontrado para o estado e período selecionados.")
else:
    # Filtra cidades se a coluna existir
    city_column = "noMunMinsgUf"  # coluna correta retornada pela API
    if city_column in df_state.columns and not df_state[city_column].dropna().empty:
        cities = sorted(df_state[city_column].dropna().unique())
        city_name = st.sidebar.selectbox("Cidade:", cities)
        df_city = df_state[df_state[city_column] == city_name]
    else:
        st.info("Não há dados de cidades detalhados para o período selecionado.")
        df_city = df_state.copy()

    st.subheader(f"Dados ({flow})")
    st.dataframe(df_city)

    # ---- Gráfico por país ----
    chart_data = (
        df_city.groupby("country")[["metricFOB", "metricKG"]]
        .sum()
        .sort_values("metricFOB", ascending=False)
    )
    st.subheader("Resumo por país")
    st.bar_chart(chart_data)

    # ---- Download CSV ----
    csv = df_city.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name=f"{state_name}_{flow}_{period_from}_{period_to}.csv",
        mime='text/csv'
    )
