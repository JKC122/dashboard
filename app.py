import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração do Streamlit
st.set_page_config(page_title="Dashboard Imobiliária", layout="wide")

# Menu para navegação entre as seções
menu = [
    "Bairros com Ofertas e Procuras",
    "Desempenho das Mídias",
    "Interesse por Tipo de Imóvel nos Bairros Mais Procurados"
]
opcao = st.sidebar.selectbox("Escolha uma opção", menu)

# Função para carregar os dados, com cache para melhorar a performance
@st.cache_data
def carregar_dados():
    file_path = 'imoveis_basecompleta.xlsx'  # Ajuste o caminho conforme necessário
    df = pd.read_excel(file_path, decimal=',')
    return df

# Carregar os dados
df = carregar_dados()

# Título do Dashboard
st.title("Dashboard - Análise Imobiliária")

if opcao == "Bairros com Ofertas e Procuras":
    st.header("Comparativo: Ofertas e Procuras nos Bairros")

    # Número de imóveis ofertados por bairro
    bairros_ofertados = df['Bairro'].value_counts().head(10)

    # Número de vezes que os bairros foram procurados (simulando com os mesmos dados)
    bairros_procurados = df['Bairro'].value_counts().head(10)

    # Unir as duas métricas (ofertas e procuras)
    bairros_comparados = pd.DataFrame({
        'Bairros': bairros_ofertados.index,
        'Ofertas': bairros_ofertados.values,
        'Procuras': bairros_procurados.values
    })

    # Criar gráfico de barras agrupadas
    fig = px.bar(
        bairros_comparados, x='Bairros', y=['Ofertas', 'Procuras'],
        labels={'value': 'Quantidade', 'variable': 'Métrica'},
        title="Comparativo entre Bairros com Mais Ofertas e Bairros Mais Procurados",
        barmode='group'  # 'group' para agrupar as barras
    )
    st.plotly_chart(fig)

elif opcao == "Desempenho das Mídias":
    st.header("Desempenho das Mídias")
    if 'Mídia' in df.columns:
        midias = df['Mídia'].value_counts()
        midias_categorias = midias[["Imovel Web", "ZAP", "Chaves Na Mão"]]
        midias_categorias["Outros"] = midias.drop(midias_categorias.index).sum()
        fig3 = px.pie(midias_categorias, values=midias_categorias.values, names=midias_categorias.index, 
                      title="Desempenho das Mídias")
        st.plotly_chart(fig3)
    else:
        st.warning("A coluna 'Mídia' não está disponível nos dados.")

elif opcao == "Interesse por Tipo de Imóvel nos Bairros Mais Procurados":
    st.header("Interesse por Tipo de Imóvel nos Bairros Mais Procurados")
    bairros_mais_procurados = df['Bairro'].value_counts().head(10).index
    df_interesse = df[df['Bairro'].isin(bairros_mais_procurados)]
    df_interesse = df_interesse.groupby(['Bairro', 'Tipo']).size().unstack().fillna(0)
    fig4 = px.bar(df_interesse, x=df_interesse.index, y=df_interesse.columns, 
                  title="Interesse por Tipo de Imóvel nos Bairros Mais Procurados", barmode='stack')
    st.plotly_chart(fig4)
