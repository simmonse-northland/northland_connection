import os
# from fpdf import FPDF
from OrderData import OrderData
from datetime import datetime
# from PIL import Image
import pdfkit


footer = datetime.now().strftime("%d:%m:%Y")

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
                        .footer {{
                            position: fixed;
                            bottom: 0;
                            width: 100%;
                            text-align: center;
                            font-size: 12px;
                            color: #888888;
                            font-family: Arial, sans-serif;
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
        html += '''
                    </table>
                </body>
            </html>
            '''
        return html
    @staticmethod
    def genertate_html_title(headers):
        html = f'''
            <html>
                <body>
                    {headers['FIRSTNAME']} {headers['LASTNAME']}<br>
                    Contract# {headers['CONTRACT']}</p>
                </body>
            </html>
            '''     
        return html

    @classmethod
    def generate_pdf(cls, filename, html):
        if not os.path.exists('pdf_reports'):
                os.makedirs('pdf_reports')
        # generate HTML content
        
        
        filename = filename.replace('/', '-')
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files (x86)/wkhtmltopdf/bin/wkhtmltopdf.exe')
        options={
            'enable-local-file-access': None,
            'page-height': '6in',
            'page-width': '4in', 
            'margin-top': "0.05in",
            'margin-right': "0.05in",
            'margin-bottom': "0.05in",
            'margin-left': "0.05in",
            }
        pdfkit.from_string(html, f'pdf_reports/{filename}', options=options, configuration=config)
        return filename
        
    @classmethod
    def generate_report_all_trim(cls, headers, data):
        html = cls.generate_html_report(headers, data)
        cls.generate_pdf("report.pdf", html)

    @classmethod
    def generate_report_title(cls, headers):
        html = cls.genertate_html_title(headers)
        cls.generate_pdf("title.pdf", html)

    @classmethod
    def generate_report_each_trim(cls, headers, contract):
        if not os.path.exists('pdf_reports'):
            os.makedirs('pdf_reports')
        grouped_trim = OrderData.get_grouped_trim(contract)

        for description, color, qty in grouped_trim:
            data = [(description, color, qty)]
            filename = f"{description} {color} {qty}".replace('/', '_').replace('"', '').replace(':', '') + ".pdf"
            cls.generate_pdf(filename, cls.generate_html_report(headers, data))