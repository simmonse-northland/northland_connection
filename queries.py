from db import execute_query

def get_headers_by_estimate_id(estimate_id):
    sql = f"""
    USE NBEstTransmitted;
    SELECT FIRSTNAME, LASTNAME, Order_Date, EstimateID
    FROM dbo.Customers_Main_tbl
    WHERE EstimateID = {estimate_id}
    """
    result = execute_query(sql)
    if result and len(result[0]) == 4:
        order_date = result[0][2].strftime('%Y-%m-%d')
        print({'FIRSTNAME': result[0][0], 'LASTNAME': result[0][1], 'Order_Date': order_date, 'EstimateID': result[0][3]})
        return {'FIRSTNAME': result[0][0], 'LASTNAME': result[0][1], 'Order_Date': order_date, 'EstimateID': result[0][3]}
    else:
        return None

def get_trim_by_estimate_id(estimate_id):
    sql = f"""
    USE NBEstTransmitted;
    SELECT Description, COLOR, ORDQTY
    FROM dbo.Customers_Detail_tbl
    WHERE EstimateID = {estimate_id} AND Category = 'Trim'
    """
    result = execute_query(sql)
    if result:
        return result
    else:
        return None