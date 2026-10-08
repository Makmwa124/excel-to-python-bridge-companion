"""Chapter 10: Running totals, ranks and change

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd

xl = "data/kestrel_sales.xlsx"
orders = pd.read_excel(xl, sheet_name="Orders")
customers = pd.read_excel(xl, sheet_name="Customers")
orders["Revenue"] = (orders["Qty"] * orders["UnitPrice"]
                     * (1 - orders["Discount"])).round(2)
orders["Month"] = orders["OrderDate"].dt.to_period("M")

monthly = (orders.groupby("Month", as_index=False)
           ["Revenue"].sum())

# --- Step 2 ---
monthly["YTD"] = monthly["Revenue"].cumsum()
monthly.head(4).round({"Revenue": 0, "YTD": 0})

# --- Step 3 ---
monthly["Change"] = monthly["Revenue"].diff()
monthly["PctChange"] = (monthly["Revenue"]
                        .pct_change() * 100)
(monthly[["Month", "Revenue", "Change", "PctChange"]]
 .head(4).round({"Revenue": 1, "Change": 1, "PctChange": 1}))

# --- Step 4 ---
monthly["LastMonth"] = monthly["Revenue"].shift(1)
monthly[["Month", "Revenue", "LastMonth"]].head(3)

# --- Step 5 ---
monthly["Avg3M"] = monthly["Revenue"].rolling(3).mean()
monthly[["Month", "Revenue", "Avg3M"]].tail(4).round(
    {"Revenue": 0, "Avg3M": 0})

# --- Step 6 ---
rep_month = (orders.groupby(["Rep", "Month"], as_index=False)
             ["Revenue"].sum())
rep_month["RepYTD"] = (rep_month.groupby("Rep")["Revenue"]
                       .cumsum())
rep_month[rep_month["Month"] == "2025-12"].round(
    {"Revenue": 0, "RepYTD": 0})

# --- Step 7 ---
cust_rev = (orders.groupby("CustomerID", as_index=False)
            ["Revenue"].sum())
cust_rev["Rank"] = (cust_rev["Revenue"]
                    .rank(ascending=False, method="min")
                    .astype(int))
cust_rev.sort_values("Rank").head(5)

# --- Step 8 ---
cust_rev = cust_rev.merge(customers[["CustomerID",
                                     "CustomerName", "State"]],
                          on="CustomerID")
cust_rev["RankInState"] = (cust_rev.groupby("State")["Revenue"]
                           .rank(ascending=False, method="min")
                           .astype(int))
(cust_rev[cust_rev["RankInState"] == 1]
 [["State", "CustomerName", "Revenue"]])

# --- Step 9 ---
(cust_rev.sort_values("Revenue", ascending=False)
         .groupby("State")
         .head(3)
         .sort_values(["State", "Revenue"],
                      ascending=[True, False])
         [["State", "CustomerName", "Revenue"]])

# --- Step 10 ---
cust_rev["Revenue"].quantile([0.25, 0.5, 0.75, 0.9]).round(0)

# --- Step 11 ---
pareto = cust_rev.sort_values("Revenue", ascending=False)
pareto["CumShare"] = (pareto["Revenue"].cumsum()
                      / pareto["Revenue"].sum() * 100)
top20 = int(len(pareto) * 0.2)
print(top20, "customers")
share = pareto["CumShare"].iloc[top20 - 1]
print(round(share, 1), "% of revenue")

