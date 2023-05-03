from db import execute_query
from fpdf import FPDF
import os
import subprocess
import datetime

# use contract number instead of estimate ID

class OrderData:
    def __init__(self, contract):
        self.contract = contract


    @classmethod
    def get_contracts(cls):
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
        

    @classmethod
    def generate_pdf(cls, headers, data, filename):
        if not os.path.exists('pdf_reports'):
            os.makedirs('pdf_reports')
        pdf = FPDF(unit='in', format=(4, 6))
        pdf.set_margins(left=0.1, top=0.1, right=0.1)
        pdf.bottom_margin = 0.1
        pdf.set_auto_page_break(True, margin=0.1)
        pdf.add_page()
        pdf.cell_margin = 0.1
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 0.2, f"{headers['FIRSTNAME']} {headers['LASTNAME']} {headers['Order_Date']} Order# {headers['CONTRACT']}", 0, 1, 'C')
        pdf.ln(0.1)
        pdf.set_font('Arial', 'B', size=10)
        col_names = ['Description', 'Color', 'Qty']
        col_widths = [1.9, 1.2, 0.4]

        for i in range(len(col_names)):
            pdf.cell(col_widths[i], 0.17, col_names[i], border=1)
        pdf.ln()

        for row in data:
            for i in range(len(row)):
                pdf.cell(col_widths[i], 0.17, str(row[i]), border=1)
            pdf.ln()

        filename = filename.replace('/', '-')
        pdf.output(name=f"pdf_reports/{filename}")

    @classmethod
    def generate_report_all_trim(cls, headers, data):
        cls.generate_pdf(headers, data, "report.pdf")

    @classmethod
    def generate_report_each_trim(cls, headers, contract):
        if not os.path.exists('pdf_reports'):
            os.makedirs('pdf_reports')
        grouped_trim = cls.get_grouped_trim(contract)

        for description, color, qty in grouped_trim:
            filename = f"{description} {color} {qty}".replace('/', '_').replace('"', '').replace(':', '') + ".pdf"
            cls.generate_pdf(headers, [(description, color, qty)], filename)


    # @classmethod
    # def print_pdf_report(cls, filename):
    #     try:
    #         printer_name = 'YOUR_PRINTER_NAME'  # replace with the name of your printer
    #         process = subprocess.Popen([f'AcroRd32.exe /t "{filename}" "{printer_name}"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #         stdout, stderr = process.communicate()
    #         if stderr:
    #             raise Exception(f"Error while printing {filename}: {stderr}")
    #         else:
    #             print(f"Successfully printed {filename}")
    #     except Exception as e:
    #         print(f"Error while printing {filename}: {e}")