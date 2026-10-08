"""Chapter 2: Sort and filter

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd

xl = "data/kestrel_sales.xlsx"
orders = pd.read_excel(xl, sheet_name="Orders")
customers = pd.read_excel(xl, sheet_name="Customers")

# --- Step 2 ---
customers.sort_values("CreditLimit", ascending=False).head()

# --- Step 3 ---
cols = ["CustomerName", "State", "CreditLimit"]
(customers[cols]
    .sort_values(["State", "CreditLimit"],
                 ascending=[True, False])
    .head())

# --- Step 4 ---
orders.nlargest(5, "Qty")[["OrderID", "ProductCode", "Qty"]]

# --- Step 5 ---
sa = customers[customers["State"] == "SA"]
len(sa)

# --- Step 6 ---
(customers["State"] == "SA").head()

# --- Step 7 ---
big = orders[orders["Qty"] >= 10]
len(big)

# --- Step 8 ---
sa_cafes = customers[(customers["State"] == "SA")
                     & (customers["Segment"] == "Cafe")]
len(sa_cafes)

# --- Step 9 ---
hotel_or_big = customers[(customers["Segment"] == "Hotel")
                         | (customers["CreditLimit"] >= 20000)]
len(hotel_or_big)

# --- Step 10 ---
east = customers[customers["State"].isin(["VIC", "NSW"])]
east["State"].value_counts()

# --- Step 11 ---
customers[customers["CustomerName"].str.contains("Hotel")][
    ["CustomerName", "Suburb"]].head()

# --- Step 12 ---
q1 = orders[orders["OrderDate"].between("2025-01-01",
                                        "2025-03-31")]
q1["OrderDate"].agg(["min", "max", "count"])

# --- Step 13 ---
orders.query("Rep == 'Tom Walsh' and Qty >= 10").shape

# --- Step 14 ---
(customers["Segment"] == "Cafe").sum()

# --- Step 15 ---
(customers["Segment"] == "Cafe").mean().round(3)

