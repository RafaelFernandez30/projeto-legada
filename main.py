import streamlit as st
import pandas as pd
import plotly.express as px
import locale
import numpy as np
import plotly.graph_objs as go

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

st.set_page_config(layout="wide")

df = pd.read_csv("ValoresProjeto.csv", sep=";", decimal=",")
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
df = df.sort_values('Data')

df['Receita'] = df['Receita'].astype(float)
df['Despesa'] = df['Despesa'].astype(float)

df["Mês"] = df["Data"].dt.strftime("%B")
segmentacao_mes = st.sidebar.selectbox("Selecione o mês", df["Mês"].unique())

df["Saldo"] = df["Receita"] - df["Despesa"]
df['Saldo'] = df['Saldo'].astype(float)

df["Dia - Mês"] = df["Data"].dt.strftime("%d de %B")

filtrar_df = df[df["Mês"] == segmentacao_mes]
st.dataframe(filtrar_df.drop(columns=["Mês"]), use_container_width=True)


def calcular_totais(dataframe):
    total_receita = dataframe['Receita'].sum()
    total_despesa = dataframe['Despesa'].sum()
    return total_receita, total_despesa


filtro = st.checkbox("Filtrar dados", value=True)
if filtro:

    df_filtrado = filtrar_df
else:
    df_filtrado = df

total_receita, total_despesa = calcular_totais(df_filtrado)

st.subheader("Total de Receita:")
st.write(f"R$ {total_receita:.2f}")

st.subheader("Total de Despesa:")
st.write(f"R$ {total_despesa:.2f}")

grafico1, grafico2 = st.columns(2)
grafico3, grafico4 = st.columns(2)

soma_saldo_por_dia = filtrar_df.groupby(["Dia - Mês", "Tipo de Conta"])["Saldo"].sum().reset_index()
receita_e_despesas_por_dia = px.bar(soma_saldo_por_dia, x="Dia - Mês", y="Saldo", color="Tipo de Conta", title="Total de Despesas por dia")
grafico1.plotly_chart(receita_e_despesas_por_dia)

apenas_receita = filtrar_df[filtrar_df["Receita"] > 0]
receita_por_categoria = px.bar(apenas_receita, x="Receita", y="Tipo do Histórico", color="Tipo do Histórico",
                               title="Total de Receita por Categoria", orientation="h")
grafico2.plotly_chart(receita_por_categoria)

despesa_pizza = pd.DataFrame(filtrar_df, columns=["Tipo do Histórico", "Despesa", "Data"])
apenas_despesa = despesa_pizza[despesa_pizza["Despesa"] > 0]
total_por_categoria = apenas_despesa.groupby('Tipo do Histórico')['Despesa'].sum().reset_index()
fig = px.pie(total_por_categoria, names='Tipo do Histórico', values='Despesa', title='Total de Despesas por Categoria')
grafico3.plotly_chart(fig)


total_por_mes = df.groupby(["Mês"])[["Receita", "Despesa"]].sum().reset_index()

grafico_linha = go.Figure()
grafico_linha.add_trace(go.Scatter(x=total_por_mes["Mês"], y=total_por_mes["Receita"], mode='lines+markers', name='Receita'))
grafico_linha.add_trace(go.Scatter(x=total_por_mes["Mês"], y=total_por_mes["Despesa"], mode='lines+markers', name='Despesa'))
grafico_linha.update_layout(title='Receita e Despesa por Mês', xaxis_title='Mês', yaxis_title='Valor')
grafico4.plotly_chart(grafico_linha)