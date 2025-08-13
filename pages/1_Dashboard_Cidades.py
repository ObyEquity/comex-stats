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

# ---- Lista de estados corrigida ----
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

# ---- DEBUG ----
st.subheader("Debug: Dados brutos do DataFrame")
st.write("Número de linhas:", len(df_state))
st.write("Colunas disponíveis:", df_state.columns.tolist())
st.dataframe(df_state.head(10))

if df_state.empty:
    st.warning("Nenhum dado encontrado para o estado e período selecionados.")
else:
    # Converter metricFOB e metricKG para float
    df_state["metricFOB"] = df_state["metricFOB"].astype(float)
    df_state["metricKG"] = df_state["metricKG"].astype(float)
    
    # Filtra cidades se existir
    city_column = "noMunMinsgUf"
    if city_column in df_state.columns and not df_state[city_column].dropna().empty:
        cities = sorted(df_state[city_column].dropna().unique())
        city_name = st.sidebar.selectbox("Cidade:", cities)
        df_city = df_state[df_state[city_column] == city_name].copy()
    else:
        st.info("Não há dados de cidades detalhados para o período selecionado.")
        df_city = df_state.copy()

    # Criar colunas formatadas
    if "metricFOB" in df_city.columns:
        df_city["metricFOB_R$mil"] = df_city["metricFOB"] / 1000

    if "metricKG" in df_city.columns:
        df_city["metricKG_mil"] = df_city["metricKG"] / 1000

    st.subheader(f"Dados detalhados ({flow})")
    st.dataframe(df_city)

    # ---- Gráfico 1: metricFOB (R$ mil) por país ----
    chart_fob = df_city.groupby("country")["metricFOB_R$mil"].sum().sort_values(ascending=False) / 1000
    st.subheader("Resumo metricFOB (R$ mil) por país")
    st.bar_chart(chart_fob)

    # ---- Gráfico 2: metricKG por país ----
    chart_kg = df_city.groupby("country")["metricKG_mil"].sum().sort_values(ascending=False)
    st.subheader("Resumo metricKG por país")
    st.bar_chart(chart_kg)

    # ---- Download CSV ----
    csv = df_city.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name=f"{state_name}_{flow}_{period_from}_{period_to}.csv",
        mime='text/csv'
    )

    # ---- Histórico mensal da cidade ----
    st.subheader("📈 Histórico mensal da cidade")
    # Criar filtro opcional por país
    countries = sorted(df_city["country"].dropna().unique())
    selected_country = st.multiselect("Filtrar por país (opcional):", countries, default=countries)
    
    df_city_filtered = df_city[df_city["country"].isin(selected_country)]
    
    months = pd.Series(1, index=df_city_filtered.index)  # todos como mês 1
    df_city_filtered["year_month"] = pd.to_datetime(df_city_filtered["year"].astype(str) + "-" + months.astype(str))
    monthly_data = df_city_filtered.groupby("year_month")[["metricFOB", "metricKG"]].sum().sort_index()
    
    # Mostrar tabela
    st.dataframe(monthly_data)
    
    # Gráfico metricFOB (R$ mil)
    st.subheader("Histórico metricFOB (R$ mil)")
    st.bar_chart(monthly_data["metricFOB"] / 1000)
    
    # Gráfico metricKG
    st.subheader("Histórico metricKG")
    st.bar_chart(monthly_data["metricKG"])



