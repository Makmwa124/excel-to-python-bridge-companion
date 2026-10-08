"""Chapter 3: Formulas become columns

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd
import numpy as np

xl = "data/kestrel_sales.xlsx"
orders = pd.read_excel(xl, sheet_name="Orders")

# --- Step 2 ---
orders["LineValue"] = orders["Qty"] * orders["UnitPrice"]
orders[["Qty", "UnitPrice", "LineValue"]].head(3)

# --- Step 3 ---
orders["Revenue"] = (orders["Qty"] * orders["UnitPrice"]
                     * (1 - orders["Discount"])).round(2)
orders["Revenue"].sum().round(2)

# --- Step 4 ---
GST_RATE = 0.10
orders["RevenueIncGST"] = (orders["Revenue"]
                           * (1 + GST_RATE)).round(2)
orders[["Revenue", "RevenueIncGST"]].head(3)

# --- Step 5 ---
orders["OrderSize"] = np.where(orders["Qty"] >= 10,
                               "Bulk", "Standard")
orders["OrderSize"].value_counts()

# --- Step 6 ---
needs_check = (orders["Qty"] >= 10) & (orders["Discount"] > 0)
orders["Review"] = np.where(needs_check, "Check", "OK")
orders["Review"].value_counts()

# --- Step 7 ---
conditions = [orders["Revenue"] >= 500,
              orders["Revenue"] >= 150]
labels = ["Large", "Medium"]
orders["LineBand"] = np.select(conditions, labels,
                               default="Small")
orders["LineBand"].value_counts()

# --- Step 8 ---
products = pd.read_excel(xl, sheet_name="Products")
p = products[["ProductCode", "ProductName"]].head(3).copy()
p["Upper"] = p["ProductName"].str.upper()          # UPPER
p["First5"] = p["ProductName"].str[:5]             # LEFT(,5)
p["Len"] = p["ProductName"].str.len()              # LEN
p["Num"] = p["ProductCode"].str[3:].astype(int)    # MID, VALUE
p

# --- Step 9 ---
p["Label"] = p["ProductCode"] + " - " + p["ProductName"]
for label in p["Label"]:
    print(label)

# --- Step 10 ---
reps = (orders["Rep"].drop_duplicates().sort_values()
        .reset_index(drop=True))
parts = reps.str.split(" ", expand=True)
parts.columns = ["First", "Last"]
parts

# --- Step 11 ---
names = products["ProductName"].str.replace("x1000", "(1,000)")
names.iloc[7:10]

# --- Step 12 ---
cups = pd.DataFrame({"Packs": [4, 6, 7, 13]})
cups["Cartons"] = np.ceil(cups["Packs"] / 6).astype(int)
cups["FullCartons"] = np.floor(cups["Packs"] / 6).astype(int)
cups

# --- Step 13 ---
t = pd.DataFrame({"Sales": [120, 0, 75], "Visits": [10, 0, 0]})
t["PerVisit"] = (t["Sales"] / t["Visits"])
t["PerVisitClean"] = (t["PerVisit"]
                      .replace([np.inf, -np.inf], np.nan)
                      .fillna(0))
t

# --- Step 14 ---
summary = orders.assign(
    Cost=lambda d: d["Qty"] * 0,
    Margin=lambda d: d["Revenue"] - d["Cost"],
)[["Revenue", "Cost", "Margin"]].head(2)
summary

# --- Step 15 ---
pd.Series([0.5, 1.5, 2.5, 3.5]).round(0).tolist()

# --- Step 16 ---
from decimal import Decimal, ROUND_HALF_UP

def excel_round(value, places=2):
    """Round like Excel's ROUND: 15 digits, halves away from 0."""
    d = Decimal(f"{value:.15g}")
    step = Decimal(1).scaleb(-places)
    return float(d.quantize(step, rounding=ROUND_HALF_UP))

raw = (orders["Qty"] * orders["UnitPrice"]
       * (1 - orders["Discount"]))
excel_rev = raw.map(excel_round)
print(excel_round(104.025), excel_round(-2.5, 0))
print(round(excel_rev.sum(), 2))
print((excel_rev != orders["Revenue"]).sum(), "lines differ")

