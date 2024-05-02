def fetch_result(mysql_conn, sql):
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()
        return result


def batch_insert(mysql_conn, sql, data):

    with mysql_conn.cursor() as cursor:
        cursor.executemany(sql, data)
        affected_rows = cursor.rowcount

    mysql_conn.commit()
    return affected_rows
