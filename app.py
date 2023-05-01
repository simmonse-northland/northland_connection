import pandas as pd
import pyodbc

server=r'NBMS3-VM'
database='NB_SQLExpress'
username='Northland'
password='4258thSt$%'
driver='{SQL Server}'

# Replace connection string placeholders with your own values
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
try:
    conn = pyodbc.connect(connection_string)
    print("Connected")
    conn.close()
except pyodbc.Error as e:
    print("Error", e)


