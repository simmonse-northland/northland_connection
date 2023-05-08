import os
# from fpdf import FPDF
from OrderData import OrderData
from datetime import datetime
# from PIL import Image
import pdfkit
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter


printed_at = datetime.now().strftime("%I:%M %p, %B %d, %Y")
DEFAULT_OPTIONS = {
    'enable-local-file-access': None,
    'page-height': '6in',
    'page-width': '4in',
    'margin-top': '0.05in',
    'margin-right': '0.05in',
    'margin-bottom': '0.25in',
    'margin-left': '0.05in',
    'footer-right': f"{printed_at}",
    'footer-left': '[page] of [topage]',
    'footer-font-size': 8,
    'footer-spacing' : 1
}

LANDSCAPE_OPTIONS = {
    'orientation': 'Landscape',
}



class GenerateReport():
    @staticmethod
    def generate_html_report(headers, data):
        # define HTML content
        logo_path = r"H:\basic_csv_transfer\CVST_Logo_512x512.png"
        
        html = f'''
            <html>
                <head>
                    <style>
                      body {{
                            margin: 0.05in;
                            }}
                        table {{
                            border-collapse: collapse;
                            width: 100%;
                            font-family: Arial, sans-serif;
                        }}
                        th, td {{
                            padding: 2px;
                            text-align: left;
                            font-weight: bold;
                            border: 1px solid #000000;
                        }}
                    </style>
                </head>
                <body>
                        <div style="display: flex; align-items: center;">
                        <p style="display: inline-block; margin-right: auto; font-size: 18px;">
                        <strong>
                        Manufactured in the USA By:<br>
                        CV Steel Trim, Inc.<br>
                        2894 58th St.<br>
                        Eau Claire, WI 54703 <br>
                        <br>
                        {headers['FIRSTNAME']} {headers['LASTNAME']}<br>
                        {headers['Order_Date']}<br>
                        Contract# {headers['CONTRACT']}</p>
                        </strong>
                        <img src="{logo_path}" width="200" height="200" style="display: inline-block; float: right;">
                    </div>
                    <table>
                        <tr>
                            <th>Description</th>
                            <th>Color</th>
                            <th>Qty</th>
                        </tr>
            '''
        # add rows to HTML table
        for row in data:
            html += f'''
                <tr>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>{row[2]}</td>
                </tr>
            '''
        # close html
        html += f'''
                    </table>
                </body>
            </html>
            '''
        return html
    @staticmethod
    def generate_html_title(headers):
        html = f'''
            <html>
                <body>
                    <div style="height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 175pt;
                        line-height: 1.2;
                        font-family: Arial, sans-serif;">
                        {headers['FIRSTNAME']} {headers['LASTNAME']}<br>
                        Contract# {headers['CONTRACT']}
                    </div>
                </body>
            </html>
        '''     
        return html

    @classmethod
    def generate_pdf(cls, filename, html, headers, options):
        if not os.path.exists(f"{headers['CONTRACT']}_trim_prints"):
                os.makedirs(f"{headers['CONTRACT']}_trim_prints")
        filename = filename.replace('/', '-')
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files (x86)/wkhtmltopdf/bin/wkhtmltopdf.exe')
        pdfkit.from_string(html, f"{headers['CONTRACT']}_trim_prints\{filename}", options=options, configuration=config)
        return filename
        
    @classmethod
    def generate_report_all_trim(cls, headers, data):
        options = dict(DEFAULT_OPTIONS)
        html = cls.generate_html_report(headers, data)
        cls.generate_pdf("Report.pdf", html, headers, options)

    @classmethod
    def generate_report_title(cls, headers):
        options = dict(DEFAULT_OPTIONS)
        options.update(LANDSCAPE_OPTIONS)
        html = cls.generate_html_title(headers)
        cls.generate_pdf("Title.pdf", html, headers, options)

    @classmethod
    def generate_report_each_trim(cls, headers, contract):
        options = dict(DEFAULT_OPTIONS)
        grouped_trim = OrderData.get_grouped_trim(contract)

        for description, color, qty in grouped_trim:
            data = [(description, color, qty)]
            filename = f"{description} {color} {qty}".replace('/', '_').replace('"', '').replace(':', '') + ".pdf"
            cls.generate_pdf(filename, cls.generate_html_report(headers, data), headers, options)

    @classmethod
    def split_pdf(cls, directory):
        files = os.listdir(directory)
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(directory, file)
                with open(pdf_path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    num_pages = len(pdf_reader.pages)
                    
                    if num_pages > 1:
                        for page_num in range(num_pages):
                            new_filename = os.path.splitext(file)[0] + f'_page{page_num+1}.pdf'
                            pdf_writer = PdfWriter()
                            pdf_writer.add_page(pdf_reader.pages[page_num])
                            pdf_writer.write(os.path.join(directory, new_filename))
                        pdf_file.close()
                        os.remove(pdf_path)
                        print(f"File {pdf_path} has been split into {num_pages} pages.")
                    else:
                        print(f"File {pdf_path} has only 1 page, no need to split.")