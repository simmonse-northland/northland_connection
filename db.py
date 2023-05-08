import pymssql
from config import DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_DATABASE
import os

server = DB_SERVER
username = DB_USERNAME
password = DB_PASSWORD
database = DB_DATABASE

def connect(db):
    try:
        conn = pymssql.connect(server=DB_SERVER, user=DB_USERNAME, password=DB_PASSWORD, database=db)
        print("Connected")
        return conn
    except pymssql.Error as e:
        print("Error", e)
        return None
    
def execute_query(db, sql, params=None):
    conn = connect(db)
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