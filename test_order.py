from OrderData import OrderData
from GenerateReport import GenerateReport
from prettytable import PrettyTable
# this one needs to wrap the color column
contract_number = 993085
# this one looks good
# contract_nnumber = 7704588
order = OrderData(contract_number)
report = GenerateReport()


contract = order.get_one_contract(contract_number)
column_names = order.get_column_names()
print(f"Column Names: {column_names}")

trim = order.get_trim(contract_number)
print(f"Trim Labels: {trim}")

headers = order.get_headers_for_trim_labels(contract_number)
print(f"Headers for Trim: {headers}")

grouped_trim = order.get_grouped_trim(contract_number)
print(grouped_trim)
if grouped_trim:
    table = PrettyTable()
    table.field_names = ["Description", "Color", "Total OrdQty"]
    for row in grouped_trim:
        table.add_row(row)
    print(table)
else:
    print("No grouped trim found for this order.")

contracts = order.get_all_contracts()
print(f"{contracts}")

report.generate_report_all_trim(headers, grouped_trim)
report.generate_report_each_trim(headers, contract_number)
print("report generated!")

# report.pdf_to_zpl()

# report.print_pdf()
# mac_address ="48:a4:93:bc:92:6a"  # Replace with the MAC address of your Zebra printer
# filename = "pdf_reports/report.pdf"  # Replace with the filename of the PDF file you want to print

# report.print_pdf(mac_address, filename)
