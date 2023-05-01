# this connects using ODBC which is not preffered

import pyodbc

try:
    connection = pyodbc.connect('DSN=NB_MS3_Data;UID=Northland;PWD=4258thSt$%')
    print('connected')
except pyodbc.Error as e:
    print("Error", e)

sql = """
    SELECT TOP 100 *
    FROM NBEstTransmitted.dbo.Customers_Detail_tbl
"""

results = connection.execute(sql).fetchall()

connection.close()

print(results)