import streamlit as st
import pandas as pd

# Carregar os dados do CSV
df = pd.read_csv("dados_challenges.csv")

st.title("Dashboard de Desafios na Adoção da Indústria 4.0/5.0")

# Filtros na barra lateral
with st.sidebar:
    st.header("Filtros")
    selected_country = st.multiselect("País", df['Country'].dropna().unique())
    selected_classification = st.multiselect("Classificação do país", df['Country Classification'].dropna().unique())
    selected_industry = st.multiselect("Indústria", df['Industry'].dropna().unique())
    selected_technology = st.multiselect("Tecnologia", df['Technology'].dropna().unique())
    selected_dimension = st.multiselect("Dimensão", df['Dimensions'].dropna().unique())
    selected_role = st.multiselect("Cliente ou Fornecedor", df['Customer-Provider'].dropna().unique())

# Aplicar filtros
filtered_df = df.copy()

if selected_country:
    filtered_df = filtered_df[filtered_df['Country'].isin(selected_country)]
if selected_classification:
    filtered_df = filtered_df[filtered_df['Country Classification'].isin(selected_classification)]
if selected_industry:
    filtered_df = filtered_df[filtered_df['Industry'].isin(selected_industry)]
if selected_technology:
    filtered_df = filtered_df[filtered_df['Technology'].isin(selected_technology)]
if selected_dimension:
    filtered_df = filtered_df[filtered_df['Dimensions'].isin(selected_dimension)]
if selected_role:
    filtered_df = filtered_df[filtered_df['Customer-Provider'].isin(selected_role)]

st.subheader("Desafios Encontrados")
st.write(f"{len(filtered_df)} resultados encontrados.")

# Exibir os resultados
for idx, row in filtered_df.iterrows():
    st.markdown(f"### {row['Country']} - {row['Industry'] or 'Setor não especificado'}")
    st.markdown(f"**Tecnologia:** {row['Technology']}")
    st.markdown(f"**Dimensões:** {row['Dimensions']}")
    st.markdown(f"**Papel:** {'Fornecedor/Cliente' if row['Customer-Provider']=='Yes' else 'Não especificado'}")
    st.markdown(f"**Desafios:** {row['Challenges']}")
    st.markdown("---")
