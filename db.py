import pymssql
server = r'NBMS3-VM\NB_SQLExpress'
username = 'Northland'
password = '4258thSt$%'
database = 'NBEstTransmitted'

def connect():
    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        print("Connected")
        return conn
    except pymssql.Error as e:
        print("Error", e)
        return None
    
def execute_query(sql):
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return result
    else:
        return None