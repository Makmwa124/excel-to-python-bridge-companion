"""Chapter 6: Pivot tables

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd

xl = "data/kestrel_sales.xlsx"
orders = pd.read_excel(xl, sheet_name="Orders")
products = pd.read_excel(xl, sheet_name="Products")
customers = pd.read_excel(xl, sheet_name="Customers")
orders["Revenue"] = (orders["Qty"] * orders["UnitPrice"]
                     * (1 - orders["Discount"])).round(2)
orders = (orders
          .merge(products[["ProductCode", "Category"]],
                 on="ProductCode", how="left")
          .merge(customers[["CustomerID", "State", "Segment"]],
                 on="CustomerID", how="left"))

# --- Step 2 ---
pt = orders.pivot_table(index="Category", columns="State",
                        values="Revenue", aggfunc="sum")
pt.round(0)

# --- Step 3 ---
pt = orders.pivot_table(index="Category", columns="State",
                        values="Revenue", aggfunc="sum",
                        margins=True, margins_name="Total")
pt.round(0)

# --- Step 4 ---
pt.drop(index="Total").sort_values("Total",
                                   ascending=False).round(0)

# --- Step 5 ---
orders["Month"] = orders["OrderDate"].dt.to_period("M")
monthly = orders.pivot_table(index="Rep", columns="Month",
                             values="Revenue", aggfunc="sum")
monthly.iloc[:, :4].round(0)

# --- Step 6 ---
orders.pivot_table(index="Segment",
                   values=["Revenue", "OrderID"],
                   aggfunc={"Revenue": "sum",
                            "OrderID": "nunique"}).round(0)

# --- Step 7 ---
pt2 = orders.pivot_table(index="State", columns="Segment",
                         values="Revenue", aggfunc="sum")
row_pct = pt2.div(pt2.sum(axis=1), axis=0) * 100
row_pct.round(1)

# --- Step 8 ---
orders.pivot_table(index="Segment", columns="Category",
                   values="Qty", aggfunc="sum",
                   fill_value=0).loc[:, ["Equipment", "Snacks"]]

# --- Step 9 ---
pd.crosstab(customers["State"], customers["Segment"],
            margins=True, margins_name="Total")

# --- Step 10 ---
q4 = orders[orders["OrderDate"] >= "2025-10-01"]
q4.pivot_table(index="Rep", values="Revenue",
               aggfunc="sum").round(0)

# --- Step 11 ---
flat = pt2.round(0).reset_index()
flat.columns.name = None
flat

