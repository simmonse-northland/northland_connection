from db import execute_query
import datetime

# use contract number instead of estimate ID

class OrderData:
    def __init__(self, contract):
        self.contract = contract

    @classmethod
    def get_one_contract(cls, contract):
        sql="""
        USE NBEstTransmitted;
        SELECT CONTRACT
        FROM dbo.Customers_Main_tbl
        WHERE CONTRACT = %s
        """
        params = (contract)
        result = execute_query(sql, params)
        if result:
            return result
        else: 
            return None
    @classmethod
    def get_all_contracts(cls):
        current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(current_date)
        sql = f"""
        SELECT DISTINCT CONTRACT 
        FROM dbo.Customers_Main_tbl 
        WHERE ReqDate >= '{current_date}'
        """
        result = execute_query(sql)
        if result:
            return result
        else: 
            return None


    @classmethod
    def get_grouped_trim(cls, contract):
        sql = """
        USE NBEstTransmitted;
        SELECT 
            Description, 
            STRING_AGG(COLOR, ', ') AS Colors, 
            SUM(ORDQTY) AS TotalQty
        FROM (
            SELECT 
                Description, 
                COLOR, 
                SUM(ORDQTY) AS ORDQTY
            FROM dbo.Customers_Detail_tbl
            WHERE CONTRACT = %s AND Category = 'Trim'
            GROUP BY Description, COLOR
        ) AS subquery
        GROUP BY Description;
        """
        params = (contract,)
        print(sql)
        result = execute_query(sql, params)
        if result:
            return result
        else:
            return None
        

    @classmethod
    def get_column_names(cls):
        sql = """
        USE NBEstTransmitted;
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'Customers_Detail_tbl'
        """
        result = execute_query(sql)
        if result:
            return [row[0] for row in result]
        else:
            return None
        
    @classmethod
    def get_headers_for_trim_labels(cls, contract):
        sql = """
        USE NBEstTransmitted;
        SELECT FIRSTNAME, LASTNAME, Order_Date, CONTRACT
        FROM dbo.Customers_Main_tbl
        WHERE CONTRACT = %s
        """
        params = (contract)
        result = execute_query(sql, params)
        if result:
            firstname, lastname, order_date, contract = result[0]
            order_date_str = order_date.strftime('%Y-%m-%d')
            return {'FIRSTNAME': firstname, 'LASTNAME': lastname, 'Order_Date': order_date_str, 'CONTRACT': contract}
        else:
            return None

    @classmethod
    def get_trim(cls, contract):
        sql = """
        USE NBEstTransmitted;
        SELECT Description, COLOR, ORDQTY
        FROM dbo.Customers_Detail_tbl
        WHERE CONTRACT = %s AND Category = 'Trim'
        """
        params = (contract)
        result = execute_query(sql, params)
        if result:
            return result
        else:
            return None