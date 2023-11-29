import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("banco.csv", sep=";", decimal=",")

dig = st.sidebar.selectbox("Diagnosticos", df["Diagnostico"].unique())

df_feltered = df[df["Diagnostico"] == dig]

st.dataframe(df)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

leucocitos = px.bar(df_feltered, x="Diagnostico", y="Leucócitos", title="Leucócitos por diagnóstico", color="Diagnostico", orientation="v")
col1.plotly_chart(leucocitos, use_container_width=True)

fig_diagnosticos = px.pie(df, names="Diagnostico", title="Distribuição de Diagnósticos", color="Diagnostico")
col2.plotly_chart(fig_diagnosticos, use_container_width=True)

df_media = df.groupby("Diagnostico")["Hemoglobina"].mean().reset_index()
fig_media = px.bar(df_media, x="Diagnostico", y="Hemoglobina", title="Média de Hemoglobina por Diagnóstico", color="Diagnostico", orientation="v")
col3.plotly_chart(fig_media, use_container_width=True)

bastonetes = px.bar(df_feltered, x="Diagnostico", y="Bastonetes", title="Bastonetes (Infecção)", color="Diagnostico", orientation="v")
col4.plotly_chart(bastonetes, use_container_width=True)






