# import project root path
import hashlib
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

import pymysql
import requests
from src.utils.mysql_utils import fetch_result, batch_insert
from datetime import datetime


def fetch_openphish_intelligence(args=None):

    # Connect to mysql
    mysql_conn = pymysql.connect(
        host=args.host,
        user=args.user,
        password=args.password,
        port=args.port,
        cursorclass=pymysql.cursors.DictCursor,
    )

    # Fetch latest openphish intelligence
    openphish_feed_txt = "https://openphish.com/feed.txt"

    response = requests.get(openphish_feed_txt)

    if response.status_code == 200:
        lines = response.text.splitlines()
    # Get latest intelligence id
    # latest_intelligence_id = fetch_result(
    #     mysql_conn,
    #     "SELECT * FROM phishing_intelligence.openphish_community_feed limit 1",
    # )
    fetch_time = datetime.now()
    batch_insert_data = [
        [url, hashlib.sha256(url.encode()).hexdigest(), fetch_time]
        for url in lines[::-1]
    ]
    affected_rows = batch_insert(
        mysql_conn,
        "INSERT IGNORE INTO phishing_intelligence.openphish_community_feed (url, url_sha256, fetch_time) VALUES (%s, %s, %s)",
        batch_insert_data,
    )
    print(f"Suucessfully fetched openphish phishing intelligence on {fetch_time} with {affected_rows} new urls")

