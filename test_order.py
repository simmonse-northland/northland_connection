from OrderData import OrderData
from prettytable import PrettyTable

order_id = 882379
order = OrderData(order_id)

# column_names = order.get_column_names()
# print(f"Column Names: {column_names}")

trim = order.get_trim(order_id)
# print(f"Trim Labels: {trim}")

headers = order.get_headers_for_trim_labels(order_id)
# print(f"Headers for Trim: {headers}")

grouped_trim = order.get_grouped_trim(order_id)
if grouped_trim:
    table = PrettyTable()
    table.field_names = ["Description", "Color", "Total OrdQty"]
    for row in grouped_trim:
        table.add_row(row)
    print(table)
else:
    print("No grouped trim found for this order.")

order.generate_report_all_trim(headers, trim)
order.generate_report_each_trim(headers, order_id)
# print("report generated!")
