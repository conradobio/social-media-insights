from apify_client import ApifyClient
import argparse
import os
import logging
from datetime import datetime
import json

import boto3
import pandas as pd
from datetime import datetime

import threading
import io
import sys

import os

from dotenv import load_dotenv
load_dotenv('./social-media-insights/.env')

APIFY_TOKEN = os.getenv('APIFY_TOKEN')
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION") 
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

raw_bucket = 'instagram-raw'
today = datetime.now().date()

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

def pull_data_api(client, extract_type, account, date):

    folder = account.split('.')[1]
    url = f"https://www.instagram.com/{account}/"

    logging.info(f"Argumentos : {extract_type, account}")
    run_input = {
        "directUrls": [
            url
        ],
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": [
                "RESIDENTIAL"
            ]
        },
        "resultsLimit": 200,
        "resultsType": extract_type, #details posts
        "searchLimit": 1,
        "searchType": "hashtag"
    }

    logging.info(f'Extracting data from {url}')
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)

    # Fetch and print actor results from the run's dataset (if there are any)
    items = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        items.append(item)
    
    logging.info(f'Data Extracted - {len(items)}')

    file_path = f"./social-media-insights/data/ic-{folder}/ic_{folder}-{extract_type}-{date}.json"
    with open(file_path, 'w') as f:
        f.write(json.dumps(items))
    logging.info(f'Loaded data to {file_path}')
    return file_path, folder

def load_s3(file_path, bucket_name, extract_type, account_name, today):
    # Starting a Session s3
    logging.info(f'Connecting to S3')
    session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_DEFAULT_REGION
        )

    s3 = session.resource("s3")
    bucket = s3.Bucket(name=bucket_name)
    logging.info(f'Connected to {bucket_name}')

    logging.info(f'Saving files to S3')
    file_name = f'ic-{account_name}/ic-{account_name}-{extract_type}_{today}.json'
    with open(file_path, 'rb') as data:
        bucket.upload_fileobj(data,
            file_name,
            Callback=UploadProgressPercentage(file_path)
            )
    logging.info(f'Saved file to S3')

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, 
                filename="./social-media-insights/logs/logs.log", 
                format="%(asctime)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(description='Extract Data from Instagram')
    parser.add_argument('--type', required=True, help='type - details / posts')
    parser.add_argument('--account', required=True, help='instagram account name')
    args = parser.parse_args()

    today = datetime.now().date()

    # Initialize the ApifyClient with your API token
    apify_token = APIFY_TOKEN
    client = ApifyClient(apify_token)

    extract_type = args.type
    account = args.account

    file_path, account_name = pull_data_api(client, extract_type, account, today)

    raw_bucket = 'instagram-raw'
    load_s3(file_path, raw_bucket, extract_type, account_name, today)