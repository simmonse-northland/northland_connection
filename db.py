import pymssql
from config import DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE
import os

server = DB_SERVER
username = DB_USERNAME
password = DB_PASSWORD
database = DB_DATABASE

def connect():
    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        print("Connected")
        return conn
    except pymssql.Error as e:
        print("Error", e)
        return None
    
def execute_query(sql, params=None):
    conn = connect()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        return result
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()