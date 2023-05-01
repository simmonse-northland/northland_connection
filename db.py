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
    
def generate_report(results):
    pdf = FPDF()
    pdf.add_page()
    # add font
    pdf.set_font('Arial', size=12)

    # Set up column headings and widths
    col_names = ['Description', 'Color', 'Order Quantity', 'First Name', 'Last Name', 'Order Date']
    col_widths = [40, 30, 30, 40, 40, 40]

    # Set up table headers
    for i in range(len(col_names)):
        pdf.cell(col_widths[i], 10, col_names[i], border=1)
    pdf.ln()

    # Add data rows to table
    for row in results:
        for i in range(len(row)):
            pdf.cell(col_widths[i], 10, str(row[i]), border=1)
        pdf.ln()

    # Output PDF file
    pdf.output(name = "report.pdf")
    
if __name__ == "__main__":
    results = get_trim_by_estimate_id(150985)
    if results:
        generate_report(results)
        print("Report Generated!")
    else:
        print("Couldn't generate report")
