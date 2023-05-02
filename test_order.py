from OrderData import OrderData

order_id = 150985
order = OrderData(order_id)

column_names = order.get_column_names()
print(f"Column Names: {column_names}")

trim = order.get_trim(order_id)
print(f"Trim Labels: {trim}")

headers = order.get_headers_for_trim_labels(order_id)
print(f"Headers for Trim: {headers}")

order.generate_report(headers, trim)
print("report generated!")
