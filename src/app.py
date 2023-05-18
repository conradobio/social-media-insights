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
from plots import area_plot
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

    # dataframes
    df = pull_data_from_s3(ANALYTICS_BUCKET, conta_insta)
    analytics_df = adjust_dataframe(df)

    # kpis
    st.markdown("""
                <style>
                div[data-testid="metric-container"] {
                background-color: rgba(0, 0, 0, 0);
                border: 1px solid rgba(28, 131, 225, 0.1);
                padding: 2% 2% 2% 2%;
                border-radius: 5px;
                color: rgb(0, 0, 0.5);
                overflow-wrap: break-word;
                }

                /* breakline for metric text         */
                div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
                overflow-wrap: break-word;
                white-space: break-spaces;
                color: black;
                }
                </style>
                """
            , unsafe_allow_html=True)

    row1_1, row1_2, row1_3 = st.columns([1,1,1])
    row1_1.metric(label='Taxa de Engajamento', value=f"{analytics_df['engagement_rate'].iat[-1]} %")
    row1_2.metric(label='Média Likes por post', value=analytics_df['average_likes'].iat[-1])
    row1_3.metric(label='Média Comentários por post', value=analytics_df['average_comments'].iat[-1])

    row2_1, row2_2, row2_3 = st.columns([1,1,1])
    row2_1.metric(label='Total Posts', value=analytics_df['number_posts'].iat[-1])
    row2_2.metric(label='Posts Essa Semana', value=0)
    row2_3.metric(label='Média Post Semanais', value=0)

    # charts
    row3_1, row3_2 = st.columns(2, gap='large')
    seguidores_fig = area_plot(df, 'data_extracao', 'followersCount', 'Seguidores por dia', 'Seguidores')
    row3_1.plotly_chart(seguidores_fig, theme="streamlit")

    novos_seguidores_fig = area_plot(analytics_df, 'dia_analise', 'daily_followers', 'Novos Seguidores por dia', 'Novos Seguidores')
    row3_2.plotly_chart(novos_seguidores_fig, theme="streamlit")

    engajamento_fig = area_plot(analytics_df, 'dia_analise', 'engagement_rate', 'Taxa de Engajamento por dia', 'Taxa Engajamento')
    st.plotly_chart(engajamento_fig, theme="streamlit")
    
    row5_1, row5_2 = st.columns([1,1], gap='large')
    likes_fig = area_plot(analytics_df, 'dia_analise', 'average_likes', 'Média de Likes por Dia', 'Likes')
    row5_1.plotly_chart(likes_fig, theme="streamlit")

    comentarios_fig = area_plot(analytics_df, 'dia_analise', 'average_comments', 'Média de Comentarios por Dia', 'Comentários')
    row5_2.plotly_chart(comentarios_fig, theme="streamlit")


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