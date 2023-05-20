import streamlit as st
from streamlit import session_state as ss

import pandas as pd
import numpy as np
from datetime import datetime

def get_data_extracao(df, col='data_extracao'):
    dias_extracao = df[col].unique()
    return dias_extracao#.sort()  

def get_metrics(df):
    number_posts = df.uid.nunique()
    average_likes = df['qtd_likes'].mean().astype('int64')
    average_comments = df['qtd_comments'].mean().astype('int64')

    # engagement rate 
    sum_likes = df['qtd_likes'].sum()
    sum_comments = df['qtd_comments'].sum()
    sum_interations = sum_comments + sum_likes
    try:
        number_followers = df[df['uid'].isna()]['followersCount'].values[0]
    except:
        number_followers = 0
    engagement_rate = round((number_followers / sum_interations) * 100, 2)
    return number_posts, average_likes, average_comments, sum_likes, sum_comments, sum_interations, number_followers, engagement_rate

def transform_day(dia):
        ts = (dia - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
        return datetime.utcfromtimestamp(ts).date().strftime('%Y-%m-%d')

def transform_dataframe(df):
    dias_extracao = get_data_extracao(df)
    analytics = []
    for dia in dias_extracao: 
        posts_filter = df.query(f'data_extracao == "{dia}"')
        number_posts, average_likes, average_comments, sum_likes, sum_comments, sum_interations, number_followers, engagement_rate = get_metrics(posts_filter)
        date = transform_day(dia)
        analytics.append({'number_posts':number_posts, 
                            'average_likes':average_likes, 
                            'average_comments':average_comments,
                            'sum_likes': sum_likes,
                            'sum_comments': sum_comments,
                            'sum_interations': sum_interations,
                            'number_followers': number_followers,
                            'engagement_rate': engagement_rate,
                            'dia_analise': date
                            })

    return pd.DataFrame(analytics).sort_values(by='dia_analise')

def adjust_dataframe(df):
    analytics_df = transform_dataframe(df)
    analytics_df = analytics_df[analytics_df['number_followers'] != 0].reset_index(drop=True)
    analytics_df['daily_followers'] = analytics_df['number_followers'].diff()
    analytics_df['daily_followers'] = analytics_df['daily_followers'].fillna(0)

    analytics_df['daily_likes'] = analytics_df['sum_likes'].diff()
    analytics_df['daily_likes'] = analytics_df['daily_likes'].fillna(0)

    analytics_df['daily_comments'] = analytics_df['sum_comments'].diff()
    analytics_df['daily_comments'] = analytics_df['daily_comments'].fillna(0)
    return analytics_df

def process_posts_df(df, dia):
    df = df.query(f'data_extracao == "{dia}"')
    posts_gp_df = df.groupby(['tipo']).agg(
                            count_posts=pd.NamedAgg(column='uid', aggfunc='count'),
                            sum_likes=pd.NamedAgg(column='qtd_likes', aggfunc=sum),
                            sum_comments=pd.NamedAgg(column='qtd_comments', aggfunc=sum),
                            mean_likes=pd.NamedAgg(column='qtd_likes', aggfunc='mean'),
                            mean_comments=pd.NamedAgg(column='qtd_comments', aggfunc='mean'),
                            ) \
                        .reset_index()
    posts_gp_df['mean_interations'] = posts_gp_df['mean_comments'] + posts_gp_df['mean_likes'] 
    followers = df['followersCount'][~df['followersCount'].isna()].values
    posts_gp_df['engagement_rate'] = (posts_gp_df['mean_interations'] / followers) * 100
    return posts_gp_df