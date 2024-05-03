from datetime import datetime
import hashlib
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

import csv
from io import StringIO
import requests
from src.utils.mysql_utils import batch_insert,fetch_result
import pymysql

def fetch_phishtank_intelligence(args=None):

    # Get phishtank latest Etag
    phishtank_database_url=f'http://data.phishtank.com/data/{args.phishtank_token}/online-valid.csv'
    headers = {
        'Accept' : '*/*',
        'User-Agent': 'phishtank/C3PO'
    }

    response = requests.head(phishtank_database_url, headers=headers, allow_redirects=True)
    head_response = response.headers
    phishtank_etag = head_response['etag'].strip('"')
    print(phishtank_etag)


    # Connect to mysql
    mysql_conn = pymysql.connect(
        host=args.host,
        user=args.user,
        password=args.password,
        port=args.port,
        cursorclass=pymysql.cursors.DictCursor,
    )

    # Get phishtank database latest Etag
    latest_info = fetch_result(
        mysql_conn,
        "SELECT phish_id, etag FROM phishing_intelligence.phishtank_database ORDER BY id DESC LIMIT 1",
    )
    latest_phish_id = latest_info['phish_id']
    phishtank_etag = latest_info['etag']

    # Compare etags from phishtank and database
    if latest_info == phishtank_etag:
        print("No new phishtank intelligence to fetch")
        return
    else:
        print("Fetching new phishtank intelligence")
        csv_response = requests.get(phishtank_database_url, headers=headers, allow_redirects=True)
        csv_response.raise_for_status()
        print(csv_response.headers)
        
        csv_data = StringIO(csv_response.text)
        reader = csv.DictReader(csv_data)
        records = [line for line in reader]

        fetch_time = datetime.now()
        batch_insert_data = [
            [
                item['phish_id'],
                item['url'],
                hashlib.sha256(item['url'].encode()).hexdigest(),
                item['phish_detail_url'],
                item['submission_time'],
                item['verified'],
                item['verification_time'],
                item['online'],
                item['target'],
                fetch_time, 
                phishtank_etag,
            ] for item in records if int(item['phish_id']) > latest_phish_id
        ][::-1]

        print(f"Find {len(batch_insert_data)} new phishtank intelligence")
        affected_rows = batch_insert(
            mysql_conn,
            "INSERT IGNORE INTO phishing_intelligence.phishtank_database (phish_id, url, url_sha256, phish_detail_url, submission_time, verified, verification_time, online, target, fetch_time, etag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            batch_insert_data,
        )
        print(f"Successfully fetched phishtank phishing intelligence on {fetch_time} with {affected_rows} new urls")

        # # Dump into csv file
        # with open('phishtank.csv', 'w', newline='', encoding='utf-8') as file:
        #     file.write(response.text)
        

    # with open('/home/shrugging/project/PhishDetect/PhishData/src/modules/phishing_intelligence/online-valid.csv', 'r') as file:
    #     reader = csv.DictReader(file)
    #     records = [line for line in reader]

    # fetch_time = datetime.now()
    # batch_insert_data = [
    #     [
    #         item['phish_id'],
    #         item['url'],
    #         hashlib.sha256(item['url'].encode()).hexdigest(),
    #         item['phish_detail_url'],
    #         item['submission_time'],
    #         item['verified'],
    #         item['verification_time'],
    #         item['online'],
    #         item['target'],
    #         fetch_time, 
    #         phishtank_etag,
    #     ] for item in records[:1000][::-1]
    # ]

    # print(batch_insert_data)

    

    mysql_conn.close()