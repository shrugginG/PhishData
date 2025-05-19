from datetime import datetime
import hashlib
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)
import pymysql

import json
import requests

from src.utils.mysql_utils import batch_insert, fetch_result


def fetch_ecrimex_phish_intelligence(page, limit, anchor, intelligences, token):
    if page > 20:
        return intelligences

    current_intelligences = get_ecrimex_phish_intelligence(page, limit, token)
    if current_intelligences and current_intelligences[-1]["id"] > anchor:
        return fetch_ecrimex_phish_intelligence(
            page + 1, limit, anchor, intelligences + current_intelligences, token
        )
    else:
        return intelligences + [
            item for item in current_intelligences if item["id"] > anchor
        ]


def get_ecrimex_phish_intelligence(page, limit, token):
    ecrimex_phish_url = f"https://ecrimex.net/api/v1/phish?page={page}&limit={limit}"
    # print(ecrimex_phish_url)
    headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}

    json_response = requests.get(ecrimex_phish_url, headers=headers)
    json_response.raise_for_status()
    # print(json_response.headers)

    json_data = json.loads(json_response.text)
    return json_data["data"]


def dump_latest_ecrimex_phish_intelligence_into_mysql(args=None):

    # Connect to mysql
    mysql_conn = pymysql.connect(
        host=args.host,
        user=args.user,
        password=args.password,
        port=args.port,
        cursorclass=pymysql.cursors.DictCursor,
    )

    latest_info = fetch_result(
        mysql_conn,
        "SELECT phish_id FROM phishing_intelligence.ecrimex_phish ORDER BY id DESC LIMIT 1",
    )

    if not latest_info:
        print("Fetching new ecrimex intelligence")

        records = get_ecrimex_phish_intelligence(1, 100, args.ecrimex_token)
        fetch_time = datetime.now()
        batch_insert_data = [
            [
                item["id"],
                item["url"],
                hashlib.sha256(item["url"].encode()).hexdigest(),
                item["discoveredAt"],
                item["brand"],
                item["confidence"],
                item["status"],
                item["ip"][0] if len(item["ip"]) > 0 else None,
                item["asn"][0] if len(item["asn"]) > 0 else None,
                item["tld"],
                item["createdAt"],
                item["updatedAt"],
                # fetch_time
            ]
            for item in records
        ][::-1]
        affected_rows = batch_insert(
            mysql_conn,
            "INSERT IGNORE INTO phishing_intelligence.ecrimex_phish (phish_id, url, url_sha256, discovered_at, brand, confidence, status, ip, asn, tld, created_at, updated_at) VALUES (%s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s))",
            batch_insert_data,
        )
        print(
            f"Successfully fetched phishtank phishing intelligence on {fetch_time} with {affected_rows} new urls"
        )

    else:
        database_latest_phish_id = latest_info["phish_id"]
        print(f"Latest phish_id in database: {database_latest_phish_id}")
        records = fetch_ecrimex_phish_intelligence(
            1, 500, database_latest_phish_id, [], args.ecrimex_token
        )

        if not records:
            print("没有新的钓鱼网站情报数据可获取")
            return

        records.sort(key=lambda x: x["id"])
        fetch_time = datetime.now()
        batch_insert_data = [
            [
                item["id"],
                item["url"],
                hashlib.sha256(item["url"].encode()).hexdigest(),
                item["discoveredAt"],
                item["brand"],
                item["confidence"],
                item["status"],
                item["ip"][0] if len(item["ip"]) > 0 else None,
                item["asn"][0] if len(item["asn"]) > 0 else None,
                item["tld"],
                item["createdAt"],
                item["updatedAt"],
                # fetch_time
            ]
            for item in records
        ]
        affected_rows = batch_insert(
            mysql_conn,
            "INSERT IGNORE INTO phishing_intelligence.ecrimex_phish (phish_id, url, url_sha256, discovered_at, brand, confidence, status, ip, asn, tld, created_at, updated_at) VALUES (%s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s), FROM_UNIXTIME(%s))",
            batch_insert_data,
        )
        print(
            f"Successfully fetched phishtank phishing intelligence on {fetch_time} with {affected_rows} new urls"
        )
