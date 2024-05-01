import os
import argparse
import pymysql

from utils.phishing_intelligence.fetch_openphish import get_openphish_feed
from utils.mysql_utils import fetch_result

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch github action secerets")
    parser.add_argument('--host', required=True, help='Database host')
    parser.add_argument('--user', required=True, help='Database user')
    parser.add_argument('--password', required=True, help='Database password')
    parser.add_argument('--port', type=int, required=True, help='Database port')
    return parser.parse_args()


if __name__ == "__main__":
    # get_openphish_feed()

    # Parse arguments
    args = parse_args()

    mysql_conn = pymysql.connect(
        host=args.host,
        user=args.user,
        password=args.password,
        port=args.port,
        cursorclass=pymysql.cursors.DictCursor
    ) 
    
    print(fetch_result(mysql_conn,'select * from benign.benign_urls limit 1'))