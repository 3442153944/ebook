import pymysql
from pymysql import DatabaseError

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'forum',
    'password': '123456',
    'db': 'forum',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


class OperateDB:
    def execute_sql(self, sql, params=None):
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
            connection.commit()
            return result
        except DatabaseError as e:
            connection.rollback()
            print(f"Error executing SQL: {e}")
            return None
        finally:
            connection.close()

    def insert_sql(self, sql, params=None):
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
            connection.commit()
            return True
        except DatabaseError as e:
            connection.rollback()
            print(f"Error executing SQL: {e}")
            return False
        finally:
            connection.close()