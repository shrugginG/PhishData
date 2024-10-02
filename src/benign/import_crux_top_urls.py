import hashlib
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pymysql
import requests
from src.utils.mysql_utils import fetch_result, batch_insert
from datetime import datetime

from config.conn import mysql_conn_info


def fetch_crux_top_urls():

    # Connect to mysql
    mysql_conn = pymysql.connect(
        host=mysql_conn_info.host,
        user=mysql_conn_info.username,
        password=mysql_conn_info.password,
        port=mysql_conn_info.port,
        cursorclass=pymysql.cursors.DictCursor,
    )

    fetch_time = datetime.now()
    with open(
        "/home/shrugging/project/PhishDetect/PhishData/data/crux_top_urls_202407.csv",
        "r",
    ) as f:
        lines = f.readlines()
        urls_ranks = [line.strip("\n").split(",") for line in lines[1:]]
        batch_insert_data = [
            [url + "/", hashlib.sha256((url + "/").encode()).hexdigest(), rank]
            for url, rank in urls_ranks
        ]

    sql = """
    INSERT INTO benign.crux_top_urls (url, url_sha256, crux_rank) VALUES (%s, %s, %s)
"""

    affected_rows = batch_insert(mysql_conn, sql, batch_insert_data)

    print(
        f"Suucessfully fetched openphish phishing intelligence on {fetch_time} with {affected_rows} new urls"
    )
    mysql_conn.close()


if __name__ == "__main__":

    fetch_crux_top_urls()
