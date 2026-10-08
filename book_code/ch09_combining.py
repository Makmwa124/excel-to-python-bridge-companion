"""Chapter 9: Combining sheets and files

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd
from pathlib import Path

xl = "data/kestrel_sales.xlsx"
orders = pd.read_excel(xl, sheet_name="Orders")
orders["Revenue"] = (orders["Qty"] * orders["UnitPrice"]
                     * (1 - orders["Discount"])).round(2)

# --- Step 2 ---
files = sorted(Path("data/monthly").glob("orders_2025_*.xlsx"))
for f in files:
    print(f.name)

# --- Step 3 ---
frames = []
for f in files:
    month = pd.read_excel(f)
    month["SourceFile"] = f.name
    frames.append(month)

q4 = pd.concat(frames, ignore_index=True)
q4.groupby("SourceFile").size()

# --- Step 4 ---
from_files = q4["Qty"].sum()
from_book = orders.loc[orders["OrderDate"] >= "2025-10-01",
                       "Qty"].sum()
print(from_files, from_book, from_files == from_book)

# --- Step 5 ---
a = pd.DataFrame({"Rep": ["Ann"], "Sales": [100]})
b = pd.DataFrame({"Sales": [250], "Rep": ["Raj"],
                  "Region": ["North"]})
pd.concat([a, b], ignore_index=True)

# --- Step 6 ---
targets = pd.read_excel(xl, sheet_name="Targets")
targets.iloc[:, :5]

# --- Step 7 ---
long = targets.melt(id_vars="Rep", var_name="Mon",
                    value_name="Target")
long.head(7)

# --- Step 8 ---
long.pivot(index="Rep", columns="Mon",
           values="Target").iloc[:, :4]

# --- Step 9 ---
long["Month"] = pd.to_datetime("2025-" + long["Mon"],
                               format="%Y-%b").dt.to_period("M")
long = long.drop(columns="Mon")
long.head(3)

# --- Step 10 ---
orders["Month"] = orders["OrderDate"].dt.to_period("M")
actual = (orders.groupby(["Rep", "Month"], as_index=False)
          ["Revenue"].sum())

perf = actual.merge(long, on=["Rep", "Month"], how="left",
                    validate="one_to_one")
perf["VsTarget"] = (perf["Revenue"] / perf["Target"]
                    * 100).round(1)
perf[perf["Month"] == "2025-12"].round({"Revenue": 0})

# --- Step 11 ---
year = perf.groupby("Rep")[["Revenue", "Target"]].sum()
year["VsTarget"] = (year["Revenue"] / year["Target"]
                    * 100).round(1)
year.round({"Revenue": 0}).sort_values("VsTarget",
                                     ascending=False)

# --- Step 12 ---
customers = pd.read_excel(xl, sheet_name="Customers")
no_orders = customers[~customers["CustomerID"]
                      .isin(orders["CustomerID"])]
no_orders[["CustomerID", "CustomerName", "JoinDate"]]

