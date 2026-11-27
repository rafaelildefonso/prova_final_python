import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Prova python", layout="wide")

df = pd.read_csv("dados_transporte_bh.csv", sep=";", decimal=",", encoding="utf-8-sig")

df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
df.columns = df.columns.astype(str).str.strip()
df["LINHA"] = df["LINHA"].astype(str).str.strip()
df["TOTAL USUARIOS"] = pd.to_numeric(df["TOTAL USUARIOS"], errors="coerce")


df_filtrado = df[["LINHA","TOTAL USUARIOS"]].copy()

df_tabela = df_filtrado

soma_df = df.groupby("LINHA")[["TOTAL USUARIOS"]].sum().reset_index()

# st.dataframe(soma_df)

df_tabela = soma_df

st.title("Prova Pyhon")

st.sidebar.header("Controles")
opcao = st.sidebar.radio("Selecione a visualização:", ["Tabela", "Gráficos"])

if opcao == "Tabela":
    st.header("Tabela")
    st.dataframe(df_tabela, use_container_width=True, hide_index=True)

elif opcao == "Gráficos":
  st.header("Gráficos")

  # Mais usuários
  st.subheader("1. Top 5 — Transportam mais usuários")
  df_ordenado = df_tabela.sort_values("TOTAL USUARIOS", ascending=False).head(5)

  fig_linha_maior = px.bar(
      df_ordenado,
      y="TOTAL USUARIOS",
      x="LINHA",
      title="Transportam mais usuários",
      template="plotly_dark",
  )
  
  st.plotly_chart(fig_linha_maior, use_container_width=True)

  # Menos usuários
  st.subheader("2. Top 5 — Transportam menos usuários")
  df_ordenado = df_tabela.sort_values("TOTAL USUARIOS", ascending=True).head(5)

  fig_linha_menor = px.bar(
      df_ordenado,
      y="TOTAL USUARIOS",
      x="LINHA",
      title="Transportam menos usuários",
      template="plotly_dark",
  )
  
  st.plotly_chart(fig_linha_menor, use_container_width=True)


# ==============================================================================
# 5. FONTE DOS DADOS (Obrigatória no painel)
# ==============================================================================
st.markdown("---")
st.caption("Fonte dos dados: dados abertos da Prefeitura de Belo Horizonte — https://dados.pbh.gov.br/")