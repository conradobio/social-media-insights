from apify_client import ApifyClient
import argparse
import os
import logging
from datetime import datetime
import json

def main(client, params, date):
    type = params.type
    account = params.account

    folder = account.split('.')[1]
    url = f"https://www.instagram.com/{account}/"

    logging.info(f"Argumentos : {type, account}")
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
        "resultsType": type, #details posts
        "searchLimit": 1,
        "searchType": "hashtag"
    }

    logging.info(f'Extracting data from {url}')
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)

    # Fetch and print actor results from the run's dataset (if there are any)
    items = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        items.append(item)

    # save dictionary to json file
    file_path = f"./data/ic-{folder}/ic_{folder}-{type}-{date}.json"
    with open(file_path, 'w') as f:
        f.write(json.dumps(items))
    logging.info(f'Loaded data to {file_path}')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, 
                filename="./logs/logs.log", 
                format="%(asctime)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(description='Extract Data from Instagram')
    parser.add_argument('--type', required=True, help='type - details / posts')
    parser.add_argument('--account', required=True, help='password for postgres')

    args = parser.parse_args()

    date = datetime.now().strftime('%Y-%m-%d')

    # Initialize the ApifyClient with your API token
    apify_token = 'apify_api_6tcrmwgn0f7RQq98V7NL47VsS63Jpx4rA7BA'
    client = ApifyClient(apify_token)

    main(client, args, date)