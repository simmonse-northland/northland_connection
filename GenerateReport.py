import os
from fpdf import FPDF
from OrderData import OrderData
from datetime import datetime
import usb.core
# from zplgrf import GRF
import subprocess
import zlib



class GenerateReport(FPDF):
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

        
    def footer(self):
        self.set_y(-0.3)
        self.set_font('Arial', "I", 8)
        current_datetime = datetime.now().strftime("%I:%M %p, %B %d, %Y")
        self.cell(0, 0.1, 'Page %s - %s' % (self.page_no(), current_datetime), 0, 0, 'C')
        

    @classmethod
    def generate_pdf(cls, headers, data, filename):
        if not os.path.exists('pdf_reports'):
            os.makedirs('pdf_reports')
        pdf = GenerateReport(unit='in', format=(4, 6))
        pdf.set_margins(left=0.1, top=0.1, right=0.1)
        # pdf.bottom_margin = 1.1
        pdf.set_auto_page_break(True, margin=0.3)
        pdf.add_page()
        pdf.image('CVST Logo 512x512.png', x=2.25, y=0.05, w=1.6)

        pdf.set_font('Arial', 'B', 12)
        
        pdf.multi_cell(0, 0.2, f"Manufactured in the USA By:\nCV Steel Trim, Inc.\n2894 58th St.\nEau Claire, Wi 54703", 0, "L")
        pdf.ln(0.1)
        pdf.multi_cell(0, 0.2, f"{headers['FIRSTNAME']} {headers['LASTNAME']}\n{headers['Order_Date']}\nContract# {headers['CONTRACT']}", 0, "L")
        pdf.y += 0.2
    # find correct widths for each column based on string width
        col_names = ['Description', 'Color', 'Qty']
   
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
