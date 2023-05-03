import os
from fpdf import FPDF
from OrderData import OrderData
from datetime import datetime
import subprocess

class GenerateReport:
    @classmethod
    def generate_pdf(cls, headers, data, filename):
        if not os.path.exists('pdf_reports'):
            os.makedirs('pdf_reports')
        pdf = FPDF(unit='in', format=(4, 6))
        pdf.set_margins(left=0.1, top=0.1, right=0.1)
        pdf.bottom_margin = 0.1
        pdf.set_auto_page_break(True, margin=0.1)
        

        pdf.add_page()
        pdf.image('CVST Logo 512x512.png', x=2.25, y=0.05, w=1.6)

        pdf.set_font('Arial', 'B', 12)
        
        pdf.multi_cell(0, 0.2, f"Manufactured in the USA By:\nCV Steel Trim, Inc.\n2894 58th St.\nEau Claire, Wi 54703", 0, "L")
        pdf.ln(0.1)
        pdf.multi_cell(0, 0.2, f"{headers['FIRSTNAME']} {headers['LASTNAME']}\n{headers['Order_Date']}\nContract# {headers['CONTRACT']}", 0, "L")
        pdf.y += 0.2
    # find correct widths for each column based on string width
        col_names = ['Description', 'Color', 'Qty']
        # max_widths = [pdf.get_string_width(col_name) for col_name in col_names]
        # for row in data:
        #     for i, cell in enumerate(row):
        #         cell_width = pdf.get_string_width(str(cell))
        #         max_widths[i] = max(max_widths[i], cell_width)
    # headers
        max_widths = [2.25, 1.2, 0.35]
        pdf.set_font('Arial', 'B', size=10)
        for i in range(len(col_names)):
            pdf.cell(max_widths[i], 0.17, col_names[i], border=1)
        pdf.ln()

    # rows
        for row in data:
            for i in range(len(row)):
                pdf.cell(max_widths[i], 0.17, str(row[i]), border=1)
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
        grouped_trim = OrderData.get_grouped_trim(contract)

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
