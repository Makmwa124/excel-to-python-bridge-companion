"""Chapter 1: Your workbook becomes a DataFrame

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd

orders = pd.read_excel("data/kestrel_sales.xlsx",
                       sheet_name="Orders")

# --- Step 2 ---
orders.head()

# --- Step 3 ---
orders.shape

# --- Step 4 ---
len(orders)

# --- Step 5 ---
orders.info()

# --- Step 6 ---
orders[["Qty", "UnitPrice", "Discount"]].describe()

# --- Step 7 ---
orders["Qty"].sum()

# --- Step 8 ---
orders[["OrderID", "OrderDate", "Qty"]].head(3)

# --- Step 9 ---
orders["Rep"].head(3)

# --- Step 10 ---
orders["Rep"].value_counts()

# --- Step 11 ---
orders["Rep"].nunique()

# --- Step 12 ---
pd.ExcelFile("data/kestrel_sales.xlsx").sheet_names

# --- Step 13 ---
customers = pd.read_excel("data/kestrel_sales.xlsx",
                          sheet_name="Customers")
products = pd.read_excel("data/kestrel_sales.xlsx",
                         sheet_name="Products")
products.head(3)

# --- Step 14 ---
book = pd.read_excel("data/kestrel_sales.xlsx", sheet_name=None)
for name, sheet in book.items():
    print(name, sheet.shape)

# --- Step 15 ---
orders_csv = pd.read_csv("data/orders.csv",
                         parse_dates=["OrderDate"])
orders_csv.shape

# --- Step 16 ---
pd.read_excel("data/product_report.xlsx").columns[:2].tolist()

# --- Step 17 ---
report = pd.read_excel(
    "data/product_report.xlsx",
    skiprows=2,      # skip the title and the blank row
    usecols="A:E",   # only columns A to E
    nrows=40,        # stop before the totals block
)
report.tail(3)

