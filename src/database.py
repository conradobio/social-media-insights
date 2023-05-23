import streamlit as st
from st_files_connection import FilesConnection

import pandas as pd
import pyarrow.parquet as pq
import s3fs
from datetime import datetime

def get_last_file(conn, bucket, account):
    files = conn.fs.ls(f"/{bucket}/{account}")
    return files[-1:][0]

def get_last_date(file):
    data_str = file.split('/')[2].split('_')[2].split('.')[0]
    return datetime.strptime(data_str, "%Y-%m-%d").date()

def connect_database():
    return st.experimental_connection('s3', type=FilesConnection)

def pull_data_from_s3(bucket, account):
    conn = connect_database()
    file_name = get_last_file(conn, bucket, account)
    data = get_last_date(file_name)

    bucket_uri = f's3://{file_name}/'

    return conn.read(bucket_uri, input_format="parquet", ttl=600), data

