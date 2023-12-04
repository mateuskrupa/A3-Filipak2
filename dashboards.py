import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from io import BytesIO
import base64
from PIL import Image as PILImage
from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage

st.set_page_config(layout="wide")

df = pd.read_csv("banco.csv", sep=";", decimal=",")

dig = st.sidebar.selectbox("Diagnosticos", df["Diagnostico"].unique())

df_filtered = df[df["Diagnostico"] == dig]

st.dataframe(df)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

leucocitos = px.bar(df_filtered, x="Diagnostico", y="Leucócitos", title="Leucócitos por diagnóstico", color="Diagnostico", orientation="v")
col1.plotly_chart(leucocitos, use_container_width=True)

fig_diagnosticos = px.pie(df, names="Diagnostico", title="Distribuição de Diagnósticos", color="Diagnostico")
col2.plotly_chart(fig_diagnosticos, use_container_width=True)

df_media = df.groupby("Diagnostico")["Hemoglobina"].mean().reset_index()
fig_media = px.bar(df_media, x="Diagnostico", y="Hemoglobina", title="Média de Hemoglobina por Diagnóstico", color="Diagnostico", orientation="v")
col3.plotly_chart(fig_media, use_container_width=True)

bastonetes = px.bar(df_filtered, x="Diagnostico", y="Bastonetes", title="Bastonetes (Infecção)", color="Diagnostico", orientation="v")
col4.plotly_chart(bastonetes, use_container_width=True)

# Adicione os botões dentro da barra lateral
export_png_button = st.sidebar.button("Exportar Gráficos em PNG")
export_excel_button = st.sidebar.button("Exportar Gráficos para Excel")


# Lógica de exportação dentro dos botões
if export_png_button:
    leucocitos = px.bar(df_filtered, x="Diagnostico", y="Leucócitos", title="Leucócitos por diagnóstico", color="Diagnostico", orientation="v")
    leucocitos_bytes = BytesIO()
    pio.write_image(leucocitos, leucocitos_bytes)
    leucocitos_bytes.seek(0)
    leucocitos_img = PILImage.open(leucocitos_bytes)
    leucocitos_img.save("leucocitos.png")

    fig_diagnosticos = px.pie(df, names="Diagnostico", title="Distribuição de Diagnósticos", color="Diagnostico")
    fig_diagnosticos_bytes = BytesIO()
    pio.write_image(fig_diagnosticos, fig_diagnosticos_bytes)
    fig_diagnosticos_bytes.seek(0)
    fig_diagnosticos_img = PILImage.open(fig_diagnosticos_bytes)
    fig_diagnosticos_img.save("fig_diagnosticos.png")

    fig_media = px.bar(df_media, x="Diagnostico", y="Hemoglobina", title="Média de Hemoglobina por Diagnóstico", color="Diagnostico", orientation="v")
    fig_media_bytes = BytesIO()
    pio.write_image(fig_media, fig_media_bytes)
    fig_media_bytes.seek(0)
    fig_media_img = PILImage.open(fig_media_bytes)
    fig_media_img.save("fig_media.png")

    bastonetes = px.bar(df_filtered, x="Diagnostico", y="Bastonetes", title="Bastonetes (Infecção)", color="Diagnostico", orientation="v")
    bastonetes_bytes = BytesIO()
    pio.write_image(bastonetes, bastonetes_bytes)
    bastonetes_bytes.seek(0)
    bastonetes_img = PILImage.open(bastonetes_bytes)
    bastonetes_img.save("bastonetes.png")

    st.success("Gráficos exportados em PNG com sucesso!")

if export_excel_button:
    leucocitos_bytes = BytesIO()
    pio.write_image(leucocitos, leucocitos_bytes)
    leucocitos_bytes.seek(0)

    fig_diagnosticos_bytes = BytesIO()
    pio.write_image(fig_diagnosticos, fig_diagnosticos_bytes)
    fig_diagnosticos_bytes.seek(0)

    fig_media_bytes = BytesIO()
    pio.write_image(fig_media, fig_media_bytes)
    fig_media_bytes.seek(0)

    bastonetes_bytes = BytesIO()
    pio.write_image(bastonetes, bastonetes_bytes)
    bastonetes_bytes.seek(0)

    wb = Workbook()
    ws = wb.active
    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['C'].width = 30
    ws.column_dimensions['D'].width = 30

    leucocitos_img = ExcelImage(leucocitos_bytes)
    fig_diagnosticos_img = ExcelImage(fig_diagnosticos_bytes)
    fig_media_img = ExcelImage(fig_media_bytes)
    bastonetes_img = ExcelImage(bastonetes_bytes)

    ws.add_image(leucocitos_img, 'A1')
    ws.add_image(fig_diagnosticos_img, 'B1')
    ws.add_image(fig_media_img, 'C1')
    ws.add_image(bastonetes_img, 'D1')

    wb.save("graficos_excel.xlsx")

    st.success("Gráficos exportados para Excel com sucesso!")