import streamlit as st
from streamlit import session_state as ss
from streamlit_option_menu import option_menu

import pandas as pd
import plotly.graph_objects as go
import pyarrow.parquet as pq
import s3fs
from st_files_connection import FilesConnection

st.set_page_config(page_title="Instagram Analytics", 
                    layout="wide")

from utils import RAW_BUCKET, ANALYTICS_BUCKET, ACCOUNTS
from database import pull_data_from_s3, TODAY
from plots import plot_seguidores_por_dia, area_plot
from process_data import adjust_dataframe

st.title("Instagram Analytics")

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Home", "Growth", "Engajamento", "Histórico"],
    icons=["house", "bar-chart-fill", "pencil-fill", "terminal"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)
col1, _, _ = st.columns(3)
conta_insta = col1.selectbox('Selecione a conta do Instagrma:', options=ACCOUNTS)

st.caption(f'Dados atualizados em {TODAY}')

if selected == "Home":
    st.header(f"Home")
    st.caption('Módulo destinado a visualição dos dados de forma gráfica')
    st.write('')
    st.info(f"Você está acessando a conta **{conta_insta}**")

    df = pull_data_from_s3(ANALYTICS_BUCKET, conta_insta)

    #seguidores_fig = plot_seguidores_por_dia(df)
    seguidores_fig = area_plot(df, 'data_extracao', 'followersCount', 'Seguidores por dia', 'Seguidores')
    st.plotly_chart(seguidores_fig, theme="streamlit")

    analytics_df = adjust_dataframe(df)
    st.dataframe(analytics_df)

    likes_fig = area_plot(analytics_df, 'dia_analise', 'average_likes', 'Média de Likes por Dia', 'Likes')
    st.plotly_chart(likes_fig, theme="streamlit")



if selected == "Growth":
    st.header(f"Growth")
    st.caption('Módulo destinado a visualição dos dados de forma gráfica')
    st.write('')
    st.info(f"Você está acessando a conta **{conta_insta}**")

if selected == "Engajamento":
    st.header(f"Engajamento")
    st.caption('Módulo destinado a visualição dos dados de forma gráfica')
    st.write('')
    st.info(f"Você está acessando a conta **{conta_insta}**")       

if selected == "Histórico":
    st.header(f"Histórico")
    st.caption('Módulo destinado a visualição dos dados de forma gráfica')
    st.write('')
    st.info(f"Você está acessando a conta **{conta_insta}**")  