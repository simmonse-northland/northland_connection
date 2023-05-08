     
# for auto adjusting column width
# max_widths = [pdf.get_string_width(col_name) for col_name in col_names]
        # for row in data:
        #     for i, cell in enumerate(row):
        #         cell_width = pdf.get_string_width(str(cell))
        #         max_widths[i] = max(max_widths[i], cell_width)




  # rows_too_wide = []
        # for j, row in enumerate(data):
        #     for i, cell in enumerate(row):
        #         if pdf.get_string_width(str(cell)) > max_widths[i]:
        #             # print(f"Row {j+1}, column {i+1} exceeds the maximum width.")
        #             if j not in rows_too_wide: 
        #                 rows_too_wide.append(j)
        # rows
        # for r, row in enumerate(data):
        #     cell_height = 0.17
        #     if r in rows_too_wide:
        #         new_cell_height = .17
        #         print(f'row is too wide{r}')
        #         for i in range(len(row)):
        #             coords = []
        #             current_x = pdf.get_x()
        #             current_y = pdf.get_y()
        #             coords.append(current_x)
        #             coords.append(current_y)
        #             print(coords)
        #             # print(current_y, "YWIDE")
        #             pdf.multi_cell(max_widths[i], new_cell_height, str(row[i]), border=1)
        #             if i == 0:
        #                 pdf.set_xy(current_x + max_widths[i], current_y)
        #             elif i == 2: 
        #                 pdf.set_xy(3.47, coords[1]-new_cell_height)


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


# def render_pdf_as_zpl(pdf_path, width_dots, height_dots, dpi):
    #     # Convert PDF to monochrome bitmap
    #     cmd = ['gs', '-sDEVICE=bmpmono', '-r{}x{}'.format(dpi, dpi), '-g{}x{}'.format(width_dots, height_dots), '-dNOPAUSE', '-dBATCH', '-dQUIET', '-sOutputFile=-', pdf_path]
    #     process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    #     bmp_data, _ = process.communicate()

    #     # Convert bitmap data to ASCII hexadecimal
    #     hex_data = bmp_data.hex()

    #     # Compress the ASCII hexadecimal data
    #     compressed_data = zlib.compress(bytes.fromhex(hex_data))

    #     # Generate ZPL code template with compressed bitmap data
    #     template = '^XA^GFA,{length},{length},{width},{data}^XZ'
    #     data = compressed_data.decode('ascii')
    #     length = len(data)
    #     width = int((width_dots + 7) / 8) * 8  # Round up to nearest byte boundary
    #     zpl_code = template.format(length=length, width=width, data=data)


    #     return zpl_code
    # def pdf_to_zpl(cls):
    #     with open(r'pdf_reports\report.pdf', 'rb') as pdf:
    #         pages = GRF.from_pdf(pdf.read(), "TEST")
    #     for grf in pages:
    #         output = grf.to_zpl()
    #         print(output)


    # def print_pdf(cls):
    #     # Find the Zebra printer by vendor ID and product ID
    #     dev = usb.core.find(idVendor=0x0A5F, idProduct=0x014E)
    #     print(dev)
    #     if dev is None:
    #         raise ValueError('Zebra printer not found')
        
    #     # Set the configuration and find the output endpoint
    #     dev.set_configuration()
    #     cfg = dev.get_active_configuration()
    #     intf = cfg[(0,0)]
    #     ep_out = usb.util.find_descriptor(intf, custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)

    #     # Send the command to switch to PDF mode
    #     ep_out.write(b'^XA^MNN^LL300^XZ')
    #     # Open the PDF file and write it to the printer
    #     with open(r'pdf_reports\report.pdf', 'rb') as pdf_file:
    #         pdf_data = pdf_file.read()
    #         ep_out.write(pdf_data)

    #     # Reset the printer and close the device handle
    #     dev.reset()
        

    # def footer(self):
    #     self.set_y(-0.3)
    #     self.set_font('Arial', "I", 8)
    #     current_datetime = datetime.now().strftime("%I:%M %p, %B %d, %Y")
    #     self.cell(0, 0.1, 'Page %s - %s' % (self.page_no(), current_datetime), 0, 0, 'C')
        

    # @classmethod
    # def generate_pdf(cls, headers, data, filename):
    #     if not os.path.exists('pdf_reports'):
    #         os.makedirs('pdf_reports')
    #     pdf = GenerateReport(unit='in', format=(4, 6))
    #     pdf.set_margins(left=0.1, top=0.1, right=0.1)
    #     pdf.bottom_margin = 1.1
    #     pdf.set_auto_page_break(True, margin=0.3)
    
    #     pdf.add_page()
    #     pdf.image('CVST_Logo_512x512.png', x=2.25, y=0.05, w=1.6)

    #     pdf.set_font('Arial', 'B', 12)
        
    #     pdf.multi_cell(0, 0.2, f"Manufactured in the USA By:\nCV Steel Trim, Inc.\n2894 58th St.\nEau Claire, Wi 54703", 0, "L")
    #     pdf.ln(0.1)
    #     pdf.multi_cell(0, 0.2, f"{headers['FIRSTNAME']} {headers['LASTNAME']}\n{headers['Order_Date']}\nContract# {headers['CONTRACT']}", 0, "L")
    #     pdf.y += 0.2
    # # find correct widths for each column based on string width
    #     col_names = ['Description', 'Color', 'Qty']
   
    # # headers
    #     max_widths = [2.15, 1.3, 0.35]
    #     pdf.set_font('Arial', 'B', size=10)
    #     for i in range(len(col_names)):
    #         pdf.cell(max_widths[i], 0.17, col_names[i], border=1)
    #     pdf.ln()
    #     for row in data:
    #         for i in range(len(row)):
    #             pdf.cell(max_widths[i], 0.17, str(row[i]), border=1)
    #         pdf.ln()

    #     filename = filename.replace('/', '-')
    #     pdf.output(name=f"pdf_reports/{filename}")


        # report.pdf_to_zpl()

# report.print_pdf()
# mac_address ="48:a4:93:bc:92:6a"  # Replace with the MAC address of your Zebra printer
# filename = "pdf_reports/report.pdf"  # Replace with the filename of the PDF file you want to print

# report.print_pdf(mac_address, filename)



    @staticmethod
    def generate_html(headers, data):
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

    @classmethod
    def generate_pdf(cls, headers, data, filename):
            if not os.path.exists('pdf_reports'):
                os.makedirs('pdf_reports')
        # generate HTML content
        html = cls.generate_html(headers, data)
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