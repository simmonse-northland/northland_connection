# This one connects without using ODBC, which is preffered. 
import pymssql


def connect():
    server = r'NBMS3-VM\NB_SQLExpress'
    username = 'Northland'
    password = '4258thSt$%'

    try:
        connection = pymssql.connect(server=server, user=username, password=password, database=database)
        print("Connected")
        return connection
    except pymssql.Error as e:
        print("Error", e)
        return None