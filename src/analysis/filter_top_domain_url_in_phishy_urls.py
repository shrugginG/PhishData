import pymysql

# from config.conn import mysql_conn_info
# from ..config.conn import mysql_conn_info
from utils.mysql_utils import fetch_result
from conf

if __name__ == "main":

    mysql_conn = pymysql.connect(
        host=mysql_conn_info.host,
        user=mysql_conn_info.username,
        password=mysql_conn_info.password,
        port=mysql_conn_info.port,
        cursorclass=pymysql.cursors.DictCursor,
    )

    query_sql = "SELECT url,url_sha256 FROM phihsy.phishy_urls"

    phishy_urls = fetch_result(mysql_conn, query_sql)

    print(phishy_urls[:10])
