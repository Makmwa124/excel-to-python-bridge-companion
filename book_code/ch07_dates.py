"""Chapter 7: Dates without the serial numbers

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd
import numpy as np

xl = "data/kestrel_sales.xlsx"
orders = pd.read_excel(xl, sheet_name="Orders")
customers = pd.read_excel(xl, sheet_name="Customers")
orders["Revenue"] = (orders["Qty"] * orders["UnitPrice"]
                     * (1 - orders["Discount"])).round(2)

# --- Step 2 ---
raw = pd.Series(["03/04/2025", "15/04/2025", "30/04/2025"])
pd.to_datetime(raw, format="%d/%m/%Y")

# --- Step 3 ---
d = orders[["OrderDate"]].head(3).copy()
d["Year"] = d["OrderDate"].dt.year
d["Month"] = d["OrderDate"].dt.month
d["Day"] = d["OrderDate"].dt.day
d["Weekday"] = d["OrderDate"].dt.day_name()
d["DayNum"] = d["OrderDate"].dt.dayofweek
d

# --- Step 4 ---
(orders.drop_duplicates("OrderID")["OrderDate"]
       .dt.day_name().value_counts())

# --- Step 5 ---
orders["OrderDate"].dt.strftime("%b-%y").head(3)

# --- Step 6 ---
orders["Month"] = orders["OrderDate"].dt.to_period("M")
orders["Quarter"] = orders["OrderDate"].dt.to_period("Q")
orders.groupby("Quarter")["Revenue"].sum().round(0)

# --- Step 7 ---
orders["FY"] = orders["OrderDate"].dt.to_period("Y-JUN")
orders.groupby("FY")["Revenue"].sum().round(0)

# --- Step 8 ---
e = orders[["OrderDate"]].iloc[[0, 1500]].copy()
e["MonthEnd"] = e["OrderDate"] + pd.offsets.MonthEnd(0)
e["MonthStart"] = e["OrderDate"].dt.to_period("M").dt.start_time
e["Plus3Months"] = e["OrderDate"] + pd.DateOffset(months=3)
e

# --- Step 9 ---
today = pd.Timestamp("2025-12-31")
customers["DaysWithUs"] = (today - customers["JoinDate"]).dt.days
customers["YearsWithUs"] = (customers["DaysWithUs"]
                            / 365.25).round(1)
customers[["CustomerName", "JoinDate", "DaysWithUs",
           "YearsWithUs"]].head(3)

# --- Step 10 ---
def whole_years(start, end):
    years = end.year - start.dt.year
    before_anniversary = ((end.month < start.dt.month) |
                          ((end.month == start.dt.month) &
                           (end.day < start.dt.day)))
    return years - before_anniversary.astype(int)

customers["FullYears"] = whole_years(customers["JoinDate"], today)
customers["FullYears"].value_counts().sort_index()

# --- Step 11 ---
holidays = ["2025-10-06", "2025-12-25", "2025-12-26"]
start = np.datetime64("2025-10-01")
end = np.datetime64("2025-12-31") + np.timedelta64(1, "D")
np.busday_count(start, end, holidays=holidays)

# --- Step 12 ---
weekly = (orders.set_index("OrderDate")["Revenue"]
          .resample("W-SUN").sum())
weekly.tail(4).round(0)

# --- Step 13 ---
cutoff = today - pd.Timedelta(days=30)
recent = orders[orders["OrderDate"] > cutoff]
recent["OrderDate"].min(), recent["OrderID"].nunique()

# --- Step 14 ---
serials = pd.Series([45658, 45838, 46022])
pd.to_datetime(serials, unit="D", origin="1899-12-30")

