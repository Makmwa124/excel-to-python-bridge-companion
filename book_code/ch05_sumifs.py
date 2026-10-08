"""Chapter 5: SUMIFS, COUNTIFS and friends

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
orders.groupby("Rep")["Revenue"].sum()

# --- Step 3 ---
mask = ((orders["Rep"] == "Tom Walsh")
        & (orders["Category"] == "Cups"))
orders.loc[mask, "Revenue"].sum().round(2)

# --- Step 4 ---
by_rep_cat = orders.groupby(["Rep", "Category"])["Revenue"].sum()
by_rep_cat.head(8)

# --- Step 5 ---
by_rep_cat.unstack().round(0)

# --- Step 6 ---
orders.groupby("Rep").agg(Lines=("OrderID", "size"),
                          Orders=("OrderID", "nunique"))

# --- Step 7 ---
seg = orders.groupby("Segment").agg(
    Revenue=("Revenue", "sum"),
    AvgLine=("Revenue", "mean"),
    BiggestLine=("Revenue", "max"),
    Customers=("CustomerID", "nunique"),
    Orders=("OrderID", "nunique"),
).round(2)
seg

# --- Step 8 ---
order_totals = orders.groupby(["OrderID", "Rep"],
                              as_index=False)["Revenue"].sum()
aov = order_totals.groupby("Rep")["Revenue"].mean().round(2)
aov.sort_values(ascending=False)

# --- Step 9 ---
rep_rev = orders.groupby("Rep")["Revenue"].sum()
share = (rep_rev / rep_rev.sum() * 100).round(1)
share.sort_values(ascending=False)

# --- Step 10 ---
orders["OrderTotal"] = (orders.groupby("OrderID")["Revenue"]
                        .transform("sum"))
orders["ShareOfOrder"] = (orders["Revenue"]
                          / orders["OrderTotal"]).round(3)
orders[["OrderID", "Revenue", "OrderTotal",
        "ShareOfOrder"]].head(4)

# --- Step 11 ---
test = pd.DataFrame({"Rep": ["Ann", None, "Ann"],
                     "Sales": [10, 20, 30]})
print(test.groupby("Rep")["Sales"].sum())
print(test.groupby("Rep", dropna=False)["Sales"].sum())

