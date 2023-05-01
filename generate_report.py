from fpdf import FPDF

def generate_report(data, headers):
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
    col_widths = [1.9, 0.6, 0.4]

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