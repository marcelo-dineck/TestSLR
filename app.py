import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados do novo CSV
df = pd.read_csv("desafios_completos_para_dashboard.csv")

st.set_page_config(layout="wide")
st.title("Desafios na Adoção de Tecnologias da Indústria 4.0 e 5.0")

st.markdown("""
Este painel permite explorar os principais desafios enfrentados por fornecedores e compradores na adoção de tecnologias da Indústria 4.0 e 5.0,
com base em uma revisão sistemática da literatura. Use os filtros para explorar os dados por país, indústria, dimensão, categoria, etc.
""")

# Filtros na barra lateral
with st.sidebar:
    st.header("Filtros")
    country = st.multiselect("País", df['Country'].dropna().unique())
    classification = st.multiselect("Classificação do país", df['Country Classification'].dropna().unique())
    industry = st.multiselect("Indústria", df['Industry'].dropna().unique())
    technology = st.multiselect("Tecnologia", df['Technology'].dropna().unique())
    dimension = st.multiselect("Dimensão (do artigo)", df['Dimensions'].dropna().unique())
    challenge_dimension = st.multiselect("Dimensão (do desafio)", df['Dimension'].dropna().unique())
    category = st.multiselect("Categoria do desafio", df['Category'].dropna().unique())
    role = st.multiselect("Fornecedor/Comprador", df['Customer-Provider'].dropna().unique())

# Aplicar filtros
filtered_df = df.copy()
if country:
    filtered_df = filtered_df[filtered_df['Country'].isin(country)]
if classification:
    filtered_df = filtered_df[filtered_df['Country Classification'].isin(classification)]
if industry:
    filtered_df = filtered_df[filtered_df['Industry'].isin(industry)]
if technology:
    filtered_df = filtered_df[filtered_df['Technology'].isin(technology)]
if dimension:
    filtered_df = filtered_df[filtered_df['Dimensions'].isin(dimension)]
if challenge_dimension:
    filtered_df = filtered_df[filtered_df['Dimension'].isin(challenge_dimension)]
if category:
    filtered_df = filtered_df[filtered_df['Category'].isin(category)]
if role:
    filtered_df = filtered_df[filtered_df['Customer-Provider'].isin(role)]

st.subheader(f"{len(filtered_df)} desafios encontrados")

# Gráficos
col1, col2 = st.columns(2)

with col1:
    chart_data = filtered_df['Dimension'].value_counts().reset_index()
    chart_data.columns = ['Dimensão do Desafio', 'Contagem']
    fig1 = px.bar(chart_data, x='Contagem', y='Dimensão do Desafio', orientation='h', title="Desafios por Dimensão")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    chart_data2 = filtered_df['Country'].value_counts().reset_index()
    chart_data2.columns = ['País', 'Contagem']
    fig2 = px.bar(chart_data2, x='Contagem', y='País', orientation='h', title="Desafios por País")
    st.plotly_chart(fig2, use_container_width=True)

# Novo gráfico: desafios por tecnologia
chart_data3 = filtered_df['Technology'].value_counts().reset_index()
chart_data3.columns = ['Tecnologia', 'Contagem']
fig3 = px.bar(chart_data3, x='Contagem', y='Tecnologia', orientation='h', title="Desafios por Tecnologia")
st.plotly_chart(fig3, use_container_width=True)

# Agrupar por desafio racionalizado
grouped = filtered_df.groupby('Title')

for title, group in grouped:
    st.markdown(f"### 🔹 {title} ({group['Article ID'].nunique()} artigo(s))")
    st.markdown(f"**Descrição:** {group['Description'].iloc[0]}")
    st.markdown(f"**Dimensão:** {group['Dimension'].iloc[0]}  |  **Categoria:** {group['Category'].iloc[0]}")
    st.markdown("**Ocorrências em diferentes contextos:**")

    for _, row in group.iterrows():
        st.markdown(f"- **Tecnologia:** {row['Technology']} | **Indústria:** {row['Industry']} | **País:** {row['Country']} ({row['Country Classification']}) | **Papel:** {'Fornecedor/Comprador' if row['Customer-Provider'] == 'Yes' else 'Não especificado'}")

    st.markdown("---")
