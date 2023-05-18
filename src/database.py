import streamlit as st
from st_files_connection import FilesConnection

import pandas as pd
import pyarrow.parquet as pq
import s3fs
from datetime import datetime

TODAY = datetime.now().date().strftime('%Y-%m-%d')

def pull_data_from_s3(bucket, account, today=TODAY):
    path = f'{account}/{account}_consolidado_{today}.parquet'
    bucket_uri = f'{bucket}/{path}'

    conn = st.experimental_connection('s3', type=FilesConnection)
    return conn.read(bucket_uri, input_format="parquet", ttl=600)

    # fs = s3fs.S3FileSystem()
    # path = f'{account}/{account}_consolidado_{today}.parquet'
    # bucket_uri = f's3://{bucket}/{path}/'
    
    # dataset = pq.ParquetDataset(bucket_uri, filesystem=fs)
    # table = dataset.read()
    # return table.to_pandas() 
