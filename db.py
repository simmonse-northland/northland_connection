import pymssql
from prettytable import PrettyTable

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

def get_trim_by_estimate_id(estimate_id):
    # sql = """
    # USE NBEstTransmitted;
    # SELECT Description, COLOR, ORDQTY
    # FROM dbo.Customers_Detail_tbl
    # WHERE EstimateID = 150985 AND Category = 'Trim'
    # """
    # sql="""
    # USE NBEstTransmitted;
    # SELECT FIRSTNAME, LASTNAME, Order_Date
    # FROM dbo.Customers_Main_tbl
    # WHERE EstimateID = 150985 """
    sql = """
        USE NBEstTransmitted;
        SELECT cdm.Description, cdm.COLOR, cdm.ORDQTY, cmt.FIRSTNAME, cmt.LASTNAME, cmt.Order_Date
        FROM dbo.Customers_Detail_tbl cdm
        JOIN dbo.Customers_Main_tbl cmt ON cdm.EstimateID = cmt.EstimateID
        WHERE cdm.EstimateID = 150985 AND cdm.Category = 'Trim'
        """
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        table = PrettyTable(['Description', 'Color', 'Order Quantity', 'col4', 'col5', 'col6'])

        # Add the data rows to the table
        for row in result:
            table.add_row(row)

        # Print the table
        print(table)
        return result
    else:
        return None
    
if __name__ == "__main__":
    get_trim_by_estimate_id(150985)
