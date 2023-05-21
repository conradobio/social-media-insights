import pandas as pd
import json
from datetime import datetime
import boto3
import os
import logging
from dotenv import load_dotenv

import threading
import io
import sys

load_dotenv('./social-media-insights/.env')

AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION") 
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

raw_bucket = 'instagram-raw'
analytics_bucket = 'intagram-analytics'
accounts = ['ic-sjcampos']#'zionsaopaulo'] ,
extract_types = ['details', 'posts']
today = datetime.now().date().strftime('%Y-%m-%d')

dias_semana = {'Sunday': 'Domingo',
'Monday':'Segunda-Feira',
'Tuesday': 'Terça-Feira', 
'Wednesday' :'Quarta-Feira', 
'Thursday': 'Quinta-Feira', 
'Friday': 'Sexta-Feira', 
'Saturday': 'Sábado', 
}

class UploadProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%) \n" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

def process_type_details(list_files, extract_type, account, s3, raw_bucket):
    df = pd.DataFrame()

    for file in list_files:
        filename, extension = os.path.splitext(file)
        if extension == '.json' and extract_type in filename and account in filename:
            obj = s3.Object(raw_bucket,file)
            data = obj.get()['Body'].read()
            data = json.loads(data)

            posts_stats = []
            date = file.split('_')[1].split('.')[0]

            temp_dict = data[0]
            for post in temp_dict.get('latestPosts'):
                link_post = post['shortCode']
                tipo = post['type']
                data_postagem = post['timestamp']
                qtd_comments = post['commentsCount']
                qtd_likes = post['likesCount']
                legenda = post['caption']
                hashtags = post['hashtags']
                
                posts_stats.append(dict(uid=link_post,
                                        tipo=tipo,
                                        data_postagem=data_postagem, 
                                        legenda=legenda,
                                        qtd_likes=qtd_likes,
                                        qtd_comments=qtd_comments,
                                        hashtags=hashtags,
                                        data_extracao=date
                                        ))
                
            posts_stats.append(dict(followersCount=temp_dict.get('followersCount'),
                                        data_extracao=date
                                        ))
            tmp_df = pd.DataFrame(posts_stats)

            df = pd.concat([df, tmp_df]).sort_values(by = "data_extracao").reset_index(drop=True)
    return df

def process_type_posts(list_files, extract_type, account, s3, raw_bucket):
    df = pd.DataFrame()

    for file in list_files:
        filename, extension = os.path.splitext(file)
        if extension == '.json' and extract_type in filename and account in filename:
            obj = s3.Object(raw_bucket,file)
            data = obj.get()['Body'].read()
            data = json.loads(data)
                
            posts_stats = []
            date = file.split('_')[1].split('.')[0]
            for post in data:
                link_post = post['shortCode']
                tipo = post['type']
                data_postagem = post['timestamp']
                qtd_comments = post['commentsCount']
                qtd_likes = post['likesCount']
                legenda = post['caption']
                hashtags = post['hashtags']
                
                posts_stats.append(dict(uid=link_post,
                                        tipo=tipo,
                                        data_postagem=data_postagem, 
                                        legenda=legenda,
                                        qtd_likes=qtd_likes,
                                        qtd_comments=qtd_comments,
                                        hashtags=hashtags,
                                        data_extracao=date
                                        ))
            
            tmp_df = pd.DataFrame(posts_stats)

            df = pd.concat([tmp_df, df]).sort_values(by = "data_extracao").reset_index(drop=True)
    return df    

def drop_duplicated_rows(df):
    return df.drop_duplicates(subset=['uid', 'tipo', 'data_postagem', 'legenda', 'data_extracao']) \
        .sort_values(by=['uid', 'data_extracao']) \
        .reset_index(drop=True)

def adjust_datetime(df, dias_semana):
    df['data_postagem'] = pd.to_datetime(df['data_postagem'])
    df['data_extracao'] = pd.to_datetime(df['data_extracao'])
    df['hora_postagem'] = df.data_postagem.dt.hour
    df['dia_postagem'] = df.data_postagem.dt.day_name()
    df['semana_postagem'] = df.data_postagem.dt.isocalendar().week
    df = df.replace({'dia_postagem': dias_semana})
    return df
    
def push_data_to_s3(s3, bucket_name, file_path, account, today):

    bucket = s3.Bucket(name=bucket_name)
    file_name = f'{account}/{account}_consolidado_{today}.parquet'
    with open(file_path, 'rb') as data:
            bucket.upload_fileobj(data,
                file_name,
                Callback=UploadProgressPercentage(file_path)
                )

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, 
            filename="./social-media-insights/logs/transform_data.log", 
            format="%(asctime)s - %(levelname)s - %(message)s")

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )

    s3 = session.resource("s3") 

    list_files = []
    for obj in s3.Bucket(raw_bucket).objects.all():
        key = obj.key
        list_files.append(key)
    
    for account in accounts:
        logging.info(account)
        logging.info(extract_types[0])
        details_df = process_type_details(list_files, extract_types[0], account, s3, raw_bucket)
        logging.info(details_df.shape)
        logging.info(extract_types[1])
        posts_df = process_type_posts(list_files, extract_types[1], account, s3, raw_bucket)   
        logging.info(posts_df.shape)

        df = pd.concat([details_df, posts_df]) \
            .sort_values(by = "data_extracao") \
            .reset_index(drop=True)  

        drop_df = drop_duplicated_rows(df)
        drop_df = adjust_datetime(drop_df, dias_semana)
        drop_df = drop_df \
                    .sort_values(by=['data_postagem', 'data_extracao']) \
                    .reset_index(drop=True) 
        logging.info(drop_df.shape)

        file_path = f'./social-media-insights/data/consolidados/{account}-consolidados_{today}.parquet'
        drop_df.to_parquet(file_path)
        logging.info('File saved to ' + file_path)

        push_data_to_s3(s3, analytics_bucket, file_path, account, today)
        logging.info('File saved to s3')
    