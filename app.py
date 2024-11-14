import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração do Streamlit
st.set_page_config(page_title="Dashboard Imobiliária", layout="wide")

# Menu para navegação
menu = ["Bairros Mais Procurados pelos Clientes", 
        "Bairros com Maior Número de Imóveis Ofertados", 
        "Desempenho das Mídias", 
        "Cadastrais de obras de construção civil por Bairros",
        "Interesse por Tipo de Imóvel nos Bairros Mais Procurados"]
opcao = st.sidebar.selectbox("Escolha uma opção", menu)

# Função para carregar os dados com cache
@st.cache_data
def carregar_dados():
    try:
        file_path = "base_jlimobiliaria.xlsx"
        df = pd.read_excel(file_path, decimal=',')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar base_jlimobiliaria.xlsx: {e}")
        return pd.DataFrame()

# Carregar os dados
df = carregar_dados()

try:
    df2 = pd.read_excel("imoveis_basecompleta.xlsx", decimal=',')
except Exception as e:
    st.error(f"Erro ao carregar imoveis_basecompleta.xlsx: {e}")
    df2 = pd.DataFrame()

try:
    df3 = pd.read_excel("base_cno_final.xlsx", decimal=',')
except Exception as e:
    st.error(f"Erro ao carregar base_cno_final.xlsx: {e}")
    df3 = pd.DataFrame()

# Limpeza de dados
if not df.empty:
    df.drop(['Cliente', 'Telefone(s)', 'Email', '$ Venda', '$ Locação', 
             'Nome do condomínio/edifício', 'Referências', 'Usuário(s)'], axis=1, inplace=True)
    df['Dt. Cadastro'] = pd.to_datetime(df['Dt. Cadastro'])
    df['Data'] = df['Dt. Cadastro'].dt.date
    df.drop('Dt. Cadastro', axis=1, inplace=True)
    df['Bairro'] = df['Região'].str.split(',').str[0]
    df.drop(['Região', 'Area'], axis=1, inplace=True)
    df.dropna(inplace=True)

# Título do Dashboard
st.title("Dashboard - Análise Imobiliária")

# Exibir diferentes seções
if opcao == "Bairros Mais Procurados pelos Clientes" and not df.empty:
    st.header("Bairros Mais Procurados pelos Clientes")
    bairros_procurados = df['Bairro'].value_counts().head(10)
    fig1 = px.bar(bairros_procurados, x=bairros_procurados.index, y=bairros_procurados.values, 
                  labels={'x': 'Bairros', 'y': 'Procuras'}, title="Top 10 Bairros Mais Procurados")
    st.plotly_chart(fig1)

elif opcao == "Bairros com Maior Número de Imóveis Ofertados" and not df2.empty:
    st.header("Bairros com Maior Número de Imóveis Ofertados")
    bairros_ofertados = df2['Bairro'].value_counts().head(10)
    fig2 = px.bar(bairros_ofertados, x=bairros_ofertados.index, y=bairros_ofertados.values, 
                  labels={'x': 'Bairros', 'y': 'Ofertas'}, title="Top 10 Bairros com Mais Ofertas de Imóveis")
    st.plotly_chart(fig2)

elif opcao == "Desempenho das Mídias" and not df.empty:
    st.header("Desempenho das Mídias")
    try:
        midias = df['Mídia'].value_counts()
        midias_categorias = midias[["Imovel Web", "ZAP", "Chaves Na Mão"]]
        midias_categorias["Outros"] = midias.drop(midias_categorias.index).sum()
        fig3 = px.pie(midias_categorias, values=midias_categorias.values, names=midias_categorias.index, 
                      title="Desempenho das Mídias")
        st.plotly_chart(fig3)
    except Exception as e:
        st.error(f"Erro ao gerar o gráfico de desempenho das mídias: {e}")

elif opcao == "Cadastrais de obras de construção civil por Bairros" and not df3.empty:
    st.header("Cadastrais de obras de construção civil por Bairros")
    construcao = df3['Bairro'].value_counts().head(10)
    fig4 = px.pie(construcao, values=construcao.values, names=construcao.index, 
                  title="Distribuição de Obras de Construção Civil por Bairros")
    st.plotly_chart(fig4)

elif opcao == "Interesse por Tipo de Imóvel nos Bairros Mais Procurados" and not df.empty:
    st.header("Interesse por Tipo de Imóvel nos Bairros Mais Procurados")
    bairros_mais_procurados = df['Bairro'].value_counts().head(10).index
    df_interesse = df[df['Bairro'].isin(bairros_mais_procurados)]
    df_interesse = df_interesse.groupby(['Bairro', 'Tipo']).size().unstack().fillna(0)
    fig5 = px.bar(df_interesse, x=df_interesse.index, y=df_interesse.columns, 
                  title="Interesse por Tipo de Imóvel nos Bairros Mais Procurados", barmode='stack')
    st.plotly_chart(fig5)
