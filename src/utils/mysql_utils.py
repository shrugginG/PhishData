def fetch_result(mysql_conn, sql):
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result