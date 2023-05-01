
GET_TRIM_BY_ESTIMATE_ID = """
SELECT Description, COLOR, ORDQTY
FROM dbo.Customers_Detail_tbl
WHERE EstimateID = 150985 AND Category = 'Trim'
"""

GET_ORDERS_BY_CUSTOMER = """
SELECT * FROM Orders
WHERE CustomerID = ?
"""

INSERT_ORDER = """
INSERT INTO Orders (OrderID, CustomerID, OrderDate)
VALUES (?, ?, ?)
"""