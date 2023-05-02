from db import execute_query
from fpdf import FPDF

# use contract number instead of estimate ID

class OrderData:
    def __init__(self, order_id):
        self.order_id = order_id

# need a method to query by each grouping of trim type
    @classmethod
    def get_trim_by_type(cls, type):
        sql=f"""
        USE NBEstTransmitted;
        SELECT"""
# go through each order and identify what types of trim there are, store this to a list
# then query each type of trim and grab associated colors and quantitys.

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
    def get_headers_for_trim_labels(cls, order_id):
        sql = """
        USE NBEstTransmitted;
        SELECT FIRSTNAME, LASTNAME, Order_Date, EstimateID
        FROM dbo.Customers_Main_tbl
        WHERE EstimateID = %s
        """
        params = (order_id)
        result = execute_query(sql, params)
        if result and len(result[0]) == 4:
            order_date = result[0][2].strftime('%Y-%m-%d')
            print({'FIRSTNAME': result[0][0], 'LASTNAME': result[0][1], 'Order_Date': order_date, 'EstimateID': result[0][3]})
            return {'FIRSTNAME': result[0][0], 'LASTNAME': result[0][1], 'Order_Date': order_date, 'EstimateID': result[0][3]}
        else:
            return None

    # @classmethod
    # def get_headers(cls, order_id):
    #     sql = """
    #     USE NBEstTransmitted;
    #     SELECT FIRSTNAME, LASTNAME, Order_Date, EstimateID
    #     FROM dbo.Customers_Main_tbl
    #     WHERE EstimateID = %s
    #     """
    #     params = (order_id,)
    #     result = execute_query(sql, params)
    #     if result and len(result) == 4:
    #         order_date = result[2].strftime('%Y-%m-%d')
    #         print({'FIRSTNAME': result[0][0], 'LASTNAME': result[0][1], 'Order_Date': order_date, 'EstimateID': result[0][3]})
    #         return {'FIRSTNAME': result[0][0], 'LASTNAME': result[0][1], 'Order_Date': order_date, 'EstimateID': result[0][3]}
    #     else:
    #         return None

    @classmethod
    def get_trim(cls, order_id):
        sql = """
        USE NBEstTransmitted;
        SELECT Description, COLOR, ORDQTY
        FROM dbo.Customers_Detail_tbl
        WHERE EstimateID = %s AND Category = 'Trim'
        """
        params = (order_id)
        result = execute_query(sql, params)
        if result:
            return result
        else:
            return None
        

    @classmethod
    def generate_report(cls, headers, data):
        pdf = FPDF(unit='in', format=(4, 6))
        pdf.set_margins(left=0.1, top=0.1, right=0.1)
        pdf.bottom_margin = 0.1
        pdf.set_auto_page_break(True, margin=0.1)
        pdf.add_page()
        # set font for headers
        pdf.cell_margin = 0.1
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 0.2, f"{headers['FIRSTNAME']} {headers['LASTNAME']} {headers['Order_Date']} Order# {headers['EstimateID']}", 0, 1, 'C')
        pdf.ln(0.1)

        # set font for table
        pdf.set_font('Arial', 'B', size=10)

        # Set up column headings and widths
        col_names = ['Description', 'Color', 'Qty']
        col_widths = [1.9, 1.2, 0.4]

        # Set up table headers
        for i in range(len(col_names)):
            pdf.cell(col_widths[i], 0.17, col_names[i], border=1)
        pdf.ln()

        # Add data rows to table
        for row in data:
            for i in range(len(row)):
                pdf.cell(col_widths[i], 0.17, str(row[i]), border=1)
            pdf.ln()

        # Output PDF file
        pdf.output(name="report.pdf")        
