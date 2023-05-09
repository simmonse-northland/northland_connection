from OrderData import OrderData
from GenerateReport import GenerateReport
from prettytable import PrettyTable
# this one needs to wrap the color column
# contract_number = 993085
contract_number = 993085
# this one looks good
# contract_nnumber = 7704588
order = OrderData(contract_number)
report = GenerateReport()


contract = order.get_one_contract(contract_number)
column_names = order.get_column_names()
trim = order.get_trim(contract_number)
headers = order.get_headers_for_trim_labels(contract_number)
grouped_trim = order.get_grouped_trim(contract_number)
if grouped_trim:
    table = PrettyTable()
    table.field_names = ["Description", "Color", "Total OrdQty"]
    for row in grouped_trim:
        table.add_row(row)
    # print(table)
# else:
#     print("No grouped trim found for this order.")

contracts = order.get_all_contracts()


report.generate_report_all_trim(headers, grouped_trim)
report.generate_report_each_trim(headers, contract_number)
report.generate_report_title(headers)
print("report generated!")
report.split_pdf('993085_trim_prints')
print('reports with multiple pages have been split!')
# report.open_foxit(fr'H:\basic_csv_transfer\{contract_number}_trim_prints')
report.open_foxit(fr'H:\basic_csv_transfer\{contract_number}_trim_prints')


