import os
from fpdf import FPDF
from OrderData import OrderData
from datetime import datetime
from PIL import Image
import pdfkit
# from zplgrf import GRF
import subprocess
import zlib
import base64

def png_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded_string}"


class GenerateReport(FPDF):
    @classmethod
    def generate_pdf(cls, headers, data, filename):
        if not os.path.exists('pdf_reports'):
            os.makedirs('pdf_reports')
        
        # Load the image file using PIL
        logo_path = r"H:\basic_csv_transfer\CVST_Logo_512x512.png"
        
        # define HTML content
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
                            border: 2px solid #000000;
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
        # close HTML content
        html += '''
                    </table>
                </body>
            </html>
            '''
        
        # convert HTML to PDF
        filename = filename.replace('/', '-')
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files (x86)/wkhtmltopdf/bin/wkhtmltopdf.exe')
        options={
            'enable-local-file-access': None,
            'page-height': '6in',
            'page-width': '4in', 
            'margin-top': "0.05in",
            'margin-right': "0.05in",
            'margin-bottom': "0.05in",
            'margin-left': "0.05in"
            }
        pdfkit.from_string(html, f'pdf_reports/{filename}', options=options, configuration=config)
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


