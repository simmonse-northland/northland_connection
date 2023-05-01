import pymssql
from prettytable import PrettyTable
from fpdf import FPDF

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
    
def get_headers_by_estimate_id(estimate_id):
    sql = f"""
    USE NBEstTransmitted;
    SELECT FIRSTNAME, LASTNAME, Order_Date, EstimateID
    FROM dbo.Customers_Main_tbl
    WHERE EstimateID = {estimate_id}
    """
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        if result and len(result[0]) == 4:
            print({'FIRSTNAME': result[0][0], 'LASTNAME': result[0][1], 'Order_Date': result[0][2], 'EstimateID': result[0][3]})
            return {'FIRSTNAME': result[0][0], 'LASTNAME': result[0][1], 'Order_Date': result[0][2], 'EstimateID': result[0][3]}
        else:
            return None

def get_trim_by_estimate_id(estimate_id):
    sql = f"""
    USE NBEstTransmitted;
    SELECT Description, COLOR, ORDQTY
    FROM dbo.Customers_Detail_tbl
    WHERE EstimateID = {estimate_id} AND Category = 'Trim'
    """
    conn = connect()
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        table = PrettyTable(['Description', 'Color', 'Order Quantity'])

        # Add the data rows to the table
        for row in result:
            table.add_row(row)

        # Print the table
        print(table)
        return result
    else:
        return None
    
def generate_report(data, headers):
    pdf = FPDF(unit='in', format=(4, 6))
    pdf.set_margins(left=0.1, top=0.1, right=0.1)
    pdf.bottom_margin = 0.1
    pdf.set_auto_page_break(True, margin=0.1)
    pdf.add_page()
    # set font for headers
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(0, 0.3, f"Report for {headers['FIRSTNAME']} {headers['LASTNAME']}", 0, 1, 'C')
    pdf.cell(0, 0.3, f"Order Date: {headers['Order_Date']}   Estimate ID: {headers['EstimateID']}", 0, 1, 'C')
    pdf.ln(0.2)

    # set font for table
    pdf.set_font('Arial', size=8)

    # Set up column headings and widths
    col_names = ['Description', 'Color', 'Order Quantity']
    col_widths = [2, 1, 0.8]

    # Set up table headers
    for i in range(len(col_names)):
        pdf.cell(col_widths[i], 0.2, col_names[i], border=1)
    pdf.ln()

    # Add data rows to table
    for row in data:
        for i in range(len(row)):
            pdf.cell(col_widths[i], 0.2, str(row[i]), border=1)
        pdf.ln()

    # Output PDF file
    pdf.output(name="report.pdf")

    
if __name__ == "__main__":
    data = get_trim_by_estimate_id(150985)
    headers = get_headers_by_estimate_id(150985)
    if data:
        generate_report(data, headers)
        print("Report Generated!")
    else:
        print("Couldn't generate report")
