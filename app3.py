# This one connects without using ODBC, which is preffered. 

import pymssql

server = r'NBMS3-VM\NB_SQLExpress'
username = 'Northland'
password = '4258thSt$%'
database = 'master'

try:
    conn = pymssql.connect(server=server, user=username, password=password, database=database)
    print("Connected")

    conn.close()
except pymssql.Error as e:
    print("Error", e)