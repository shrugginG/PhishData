import os
import pymysql

from utils.phishing_intelligence.fetch_openphish import get_openphish_feed
from utils.mysql_utils import fetch_result


if __name__ == "__main__":
    # get_openphish_feed()
    print(
        os.getenv('MYSQL_HOST'),
        os.getenv('MYSQL_USER'),
        os.getenv('MYSQL_PASSWORD'),
        os.getenv('MYSQL_PORT')
    )
    # mysql_conn = pymysql.connect(
    #     host=os.getenv('MYSQL_HOST'),
    #     user=os.getenv('MYSQL_USER'),
    #     password=os.getenv('MYSQL_PASSWORD'),
    #     port=os.getenv('MYSQL_PORT'),
    #     cursorclass=pymysql.cursors.DictCursor
    # ) 
    # print(fetch_result(mysql_conn,'select * from benign.benign_urls limit 1'))