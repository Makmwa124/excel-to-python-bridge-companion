"""Appendix C: Answers to the "Try it" exercises

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

xl = "data/kestrel_sales.xlsx"
orders = pd.read_excel(xl, sheet_name="Orders")
customers = pd.read_excel(xl, sheet_name="Customers")
products = pd.read_excel(xl, sheet_name="Products")
orders["Revenue"] = (orders["Qty"] * orders["UnitPrice"]
                     * (1 - orders["Discount"])).round(2)

# --- Step 2 ---
customers["State"].value_counts()

# --- Step 3 ---
customers["CreditLimit"].max()

# --- Step 4 ---
sa = customers[customers["State"] == "SA"]
sa.nlargest(5, "CreditLimit")[["CustomerName", "CreditLimit"]]

# --- Step 5 ---
mask = ((orders["Rep"] == "Hannah Lee")
        & (orders["OrderDate"] >= "2025-12-01"))
mask.sum()

# --- Step 6 ---
customers["Tier"] = np.select(
    [customers["CreditLimit"] >= 10000,
     customers["CreditLimit"] >= 5000],
    ["Gold", "Silver"], default="Bronze")
customers["Tier"].value_counts()

# --- Step 7 ---
customers["Label"] = (customers["CustomerName"].str.upper()
                      + " (" + customers["State"] + ")")
customers["Label"].head(3)

# --- Step 8 ---
seg = orders.merge(customers[["CustomerID", "Segment"]],
                   on="CustomerID", how="left",
                   validate="many_to_one")
seg.groupby("Segment")["Revenue"].sum().sort_values(
    ascending=False).round(2)

# --- Step 9 ---
customers["CreditBand"] = pd.cut(
    customers["CreditLimit"], bins=[0, 5000, 10000, np.inf],
    labels=["Low", "Medium", "High"], right=False)
customers["CreditBand"].value_counts().sort_index()

# --- Step 10 ---
o = orders.merge(customers[["CustomerID", "State"]],
                 on="CustomerID", how="left")
print(o.groupby("State")["Revenue"].sum().round(2))
per_order = o.groupby(["OrderID", "State"],
                      as_index=False)["Revenue"].sum()
per_order.groupby("State")["Revenue"].mean().round(2)

# --- Step 11 ---
o = orders.merge(products[["ProductCode", "Category"]],
                 on="ProductCode", how="left")
o.groupby("Category")["CustomerID"].nunique()

# --- Step 12 ---
o = (orders
     .merge(products[["ProductCode", "Category"]],
            on="ProductCode", how="left")
     .merge(customers[["CustomerID", "Segment"]],
            on="CustomerID", how="left"))
units = o.pivot_table(index="Category", columns="Segment",
                      values="Qty", aggfunc="sum",
                      margins=True, margins_name="Total")
units

# --- Step 13 ---
(units.loc["Cups"] / units.loc["Total"] * 100).round(1)

# --- Step 14 ---
by_month = (orders.groupby(orders["OrderDate"]
                           .dt.to_period("M"))
            ["OrderID"].nunique())
by_month.idxmax(), by_month.max()

# --- Step 15 ---
last = (orders.groupby("CustomerID", as_index=False)
        ["OrderDate"].max())
last["DaysSince"] = (pd.Timestamp("2025-12-31")
                     - last["OrderDate"]).dt.days
last = last.merge(customers[["CustomerID", "CustomerName"]],
                  on="CustomerID")
last.nlargest(3, "DaysSince")

# --- Step 16 ---
raw = pd.read_excel("data/customer_export_messy.xlsx")
raw["State"].nunique(), raw["State"].str.upper().nunique()

# --- Step 17 ---
from pathlib import Path
files = sorted(Path("data/monthly").glob("orders_2025_*.xlsx"))
q4 = pd.concat([pd.read_excel(f) for f in files],
               ignore_index=True)
q4["Revenue"] = (q4["Qty"] * q4["UnitPrice"]
                 * (1 - q4["Discount"])).round(2)
q4.groupby(q4["OrderDate"].dt.to_period("M"))["Revenue"].sum()

# --- Step 18 ---
orders["Month"] = orders["OrderDate"].dt.to_period("M")
monthly = (orders.groupby("Month", as_index=False)
           ["Revenue"].sum())
monthly["Share"] = (monthly["Revenue"]
                    / monthly["Revenue"].sum() * 100).round(1)
monthly.tail(3)

# --- Step 19 ---
rm = (orders.groupby(["Rep", "Month"], as_index=False)
      ["Revenue"].sum())
(rm.sort_values("Revenue", ascending=False)
   .groupby("Rep").head(1)
   .sort_values("Rep"))

# --- Step 20 ---
by_rep = orders.groupby("Rep")["Revenue"].sum().sort_values()
ax = by_rep.plot.barh(color="#555555", figsize=(6, 2.6))
ax.set_title("Revenue by rep, 2025")
ax.set_ylabel("")
plt.show()

# --- Step 21 ---
o = orders.merge(customers[["CustomerID", "State"]],
                 on="CustomerID", how="left")
by_rep = (o.groupby("Rep", as_index=False)
          .agg(Orders=("OrderID", "nunique"),
               Revenue=("Revenue", "sum")))
by_state = o.groupby("State", as_index=False)["Revenue"].sum()

from pathlib import Path
Path("output").mkdir(exist_ok=True)
with pd.ExcelWriter("output/kestrel_2025.xlsx",
                    engine="xlsxwriter") as writer:
    by_rep.to_excel(writer, sheet_name="By rep", index=False)
    by_state.to_excel(writer, sheet_name="By state",
                      index=False)
    money = writer.book.add_format({"num_format": "$#,##0.00"})
    ws = writer.sheets["By rep"]
    ws.set_column("A:A", 18)
    ws.set_column("C:C", 14, money)
pd.ExcelFile("output/kestrel_2025.xlsx").sheet_names

