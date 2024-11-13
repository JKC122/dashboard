import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração do Streamlit deve ser a primeira linha do código
st.set_page_config(page_title="Dashboard Imobiliária", layout="wide")

# Menu para navegação entre as seções
menu = ["Bairros Mais Procurados pelos Clientes", 
        "Bairros com Maior Número de Imóveis Ofertados", 
        "Desempenho das Mídias", 
        "Interesse por Tipo de Imóvel nos Bairros Mais Procurados"]
opcao = st.sidebar.selectbox("Escolha uma opção", menu)

# Função para carregar os dados, com cache para melhorar a performance
@st.cache_data
def carregar_dados():
    file_path = "base_jlimobiliaria.xlsx"  # Ajuste conforme necessário
    df = pd.read_excel(file_path, decimal=',')
    return df

# Carregar os dados
df = carregar_dados()

# Título do Dashboard
st.title("Dashboard - Análise Imobiliária")

# Exibir diferentes seções de acordo com a opção escolhida no menu
if opcao == "Bairros Mais Procurados pelos Clientes":
    st.header("Bairros Mais Procurados pelos Clientes")
    bairros_procurados = df['Região'].value_counts().head(10)
    fig1 = px.bar(bairros_procurados, x=bairros_procurados.index, y=bairros_procurados.values, 
                  labels={'x': 'Bairros', 'y': 'Procuras'}, title="Top 10 Bairros Mais Procurados")
    st.plotly_chart(fig1)

elif opcao == "Bairros com Maior Número de Imóveis Ofertados":
    st.header("Bairros com Maior Número de Imóveis Ofertados")
    bairros_ofertados = df['Região'].value_counts().head(10)
    fig2 = px.bar(bairros_ofertados, x=bairros_ofertados.index, y=bairros_ofertados.values, 
                  labels={'x': 'Bairros', 'y': 'Ofertas'}, title="Top 10 Bairros com Mais Ofertas de Imóveis")
    st.plotly_chart(fig2)

elif opcao == "Desempenho das Mídias":
    st.header("Desempenho das Mídias")
    midias = df['Mídia'].value_counts()
    midias_categorias = midias[["Imovel Web", "ZAP", "Chaves Na Mão"]]
    midias_categorias["Outros"] = midias.drop(midias_categorias.index).sum()
    fig3 = px.pie(midias_categorias, values=midias_categorias.values, names=midias_categorias.index, 
                  title="Desempenho das Mídias")
    st.plotly_chart(fig3)

elif opcao == "Interesse por Tipo de Imóvel nos Bairros Mais Procurados":
    st.header("Interesse por Tipo de Imóvel nos Bairros Mais Procurados")
    bairros_mais_procurados = df['Região'].value_counts().head(10).index
    df_interesse = df[df['Região'].isin(bairros_mais_procurados)]
    df_interesse = df_interesse.groupby(['Região', 'Tipo']).size().unstack().fillna(0)
    fig4 = px.bar(df_interesse, x=df_interesse.index, y=df_interesse.columns, 
                  title="Interesse por Tipo de Imóvel nos Bairros Mais Procurados", barmode='stack')
    st.plotly_chart(fig4)