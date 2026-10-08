"""Chapter 4: Goodbye VLOOKUP

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd
import numpy as np

xl = "data/kestrel_sales.xlsx"
orders = pd.read_excel(xl, sheet_name="Orders")
products = pd.read_excel(xl, sheet_name="Products")
customers = pd.read_excel(xl, sheet_name="Customers")
orders["Revenue"] = (orders["Qty"] * orders["UnitPrice"]
                     * (1 - orders["Discount"])).round(2)

# --- Step 2 ---
lookup = products[["ProductCode", "ProductName"]]
o = orders.merge(lookup, on="ProductCode", how="left")
o[["OrderID", "ProductCode", "ProductName"]].head(3)

# --- Step 3 ---
cols = ["ProductCode", "ProductName", "Category", "UnitCost"]
o = orders.merge(products[cols], on="ProductCode", how="left")
o.shape

# --- Step 4 ---
o["COGS"] = o["Qty"] * o["UnitCost"]
o["Margin"] = o["Revenue"] - o["COGS"]
o[["Revenue", "COGS", "Margin"]].sum().round(2)

# --- Step 5 ---
o[o["ProductName"].isna()][["OrderID", "ProductCode", "Qty"]]

# --- Step 6 ---
o["Margin"].isna().sum()

# --- Step 7 ---
check = orders.merge(products[["ProductCode"]],
                     on="ProductCode", how="left",
                     indicator=True)
check["_merge"].value_counts()

# --- Step 8 ---
o["ProductName"] = o["ProductName"].fillna("Unknown product")
gone = o["ProductCode"] == "KS-099"
o.loc[gone, "ProductName"].unique().tolist()

# --- Step 9 ---
name_of = products.set_index("ProductCode")["ProductName"]
orders["ProductCode"].map(name_of).head(3)

# --- Step 10 ---
state_names = {"SA": "South Australia",
               "VIC": "Victoria",
               "NSW": "New South Wales",
               "WA": "Western Australia"}
customers["State"].map(state_names).value_counts()

# --- Step 11 ---
cust = customers.rename(columns={"CustomerID": "CustNo"})
o2 = orders.merge(cust[["CustNo", "CustomerName", "State"]],
                  left_on="CustomerID", right_on="CustNo",
                  how="left")
o2[["CustomerID", "CustNo", "CustomerName", "State"]].head(3)

# --- Step 12 ---
rebates = pd.DataFrame({
    "Category": ["Coffee", "Coffee", "Cups"],
    "State": ["SA", "VIC", "SA"],
    "RebatePct": [0.02, 0.03, 0.015],
})
o3 = (orders
      .merge(products[["ProductCode", "Category"]],
             on="ProductCode", how="left")
      .merge(customers[["CustomerID", "State"]],
             on="CustomerID", how="left")
      .merge(rebates, on=["Category", "State"], how="left"))
o3["RebatePct"] = o3["RebatePct"].fillna(0)
o3.groupby(["Category", "State"])["RebatePct"].first().loc[
    ["Coffee", "Cups"]]

# --- Step 13 ---
freight = pd.read_excel(xl, sheet_name="Freight")
freight

# --- Step 14 ---
order_value = (orders.groupby("OrderID", as_index=False)
               ["Revenue"].sum())
order_value = order_value.sort_values("Revenue")
freight["MinOrderValue"] = freight["MinOrderValue"].astype(float)
banded = pd.merge_asof(order_value, freight,
                       left_on="Revenue",
                       right_on="MinOrderValue")
banded.sort_values("OrderID").head()

# --- Step 15 ---
banded["Band"].value_counts()

# --- Step 16 ---
bins = [0, 150, 400, 1000, np.inf]
names = ["Small", "Standard", "Large", "Free"]
order_value["Band"] = pd.cut(order_value["Revenue"], bins=bins,
                             labels=names, right=False)
order_value["Band"].value_counts().sort_index()

# --- Step 17 ---
dup = pd.concat([products, products.iloc[[0]]])
bad = orders.merge(dup[["ProductCode", "ProductName"]],
                   on="ProductCode", how="left")
len(orders), len(bad)

# --- Step 18 ---
try:
    orders.merge(dup[["ProductCode", "ProductName"]],
                 on="ProductCode", how="left",
                 validate="many_to_one")
except Exception as e:
    print(type(e).__name__)

