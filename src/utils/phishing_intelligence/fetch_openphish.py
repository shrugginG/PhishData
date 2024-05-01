import pymysql
import requests
import sys
import os

openphish_feed_txt = "https://openphish.com/feed.txt"

def get_openphish_feed():
    response  = requests.get(openphish_feed_txt)

    if response.status_code == 200:
        lines = response.text.splitlines()
        print(lines)
