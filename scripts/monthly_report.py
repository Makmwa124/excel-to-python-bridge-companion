"""Kestrel Supplies monthly sales report.

Run from the companion folder:
    python scripts/monthly_report.py 2025-12
"""
import sys
from pathlib import Path

import pandas as pd

DATA = Path("data/kestrel_sales.xlsx")
OUT = Path("output")

def load_data(path=DATA):
    """Read the workbook and return orders and targets."""
    sheets = pd.read_excel(path, sheet_name=None)
    orders = sheets["Orders"]
    orders["Revenue"] = (orders["Qty"] * orders["UnitPrice"]
                         * (1 - orders["Discount"])).round(2)
    prod_cols = ["ProductCode", "ProductName", "UnitCost"]
    orders = orders.merge(sheets["Products"][prod_cols],
                          on="ProductCode", how="left",
                          validate="many_to_one")
    orders["Margin"] = (orders["Revenue"]
                        - orders["Qty"] * orders["UnitCost"])
    orders["Month"] = orders["OrderDate"].dt.to_period("M")

    year = orders["OrderDate"].dt.year.max()
    targets = sheets["Targets"].melt(
        id_vars="Rep", var_name="Mon", value_name="Target")
    targets["Month"] = pd.to_datetime(
        str(year) + "-" + targets["Mon"],
        format="%Y-%b").dt.to_period("M")
    return orders, targets.drop(columns="Mon")

def headline(df):
    """Headline numbers for a set of order lines."""
    known = df["UnitCost"].notna()
    return {
        "Revenue": df["Revenue"].sum(),
        "Orders": df["OrderID"].nunique(),
        "Customers": df["CustomerID"].nunique(),
        "Avg order": (df["Revenue"].sum()
                      / df["OrderID"].nunique()),
        "Margin %": (df.loc[known, "Margin"].sum()
                     / df.loc[known, "Revenue"].sum() * 100),
    }

def build_tables(orders, targets, month):
    """Return the report tables for one month, e.g. '2025-12'."""
    month = pd.Period(month, freq="M")
    this = orders[orders["Month"] == month]
    prev = orders[orders["Month"] == month - 1]

    summary = pd.DataFrame({"This month": headline(this),
                            "Last month": headline(prev)})
    summary["Change %"] = (summary["This month"]
                           / summary["Last month"] - 1) * 100

    reps = (this.groupby("Rep", as_index=False)["Revenue"].sum()
            .merge(targets[targets["Month"] == month],
                   on="Rep", how="left")
            .drop(columns="Month"))
    reps["Vs target %"] = reps["Revenue"] / reps["Target"] * 100

    top = (this.groupby("ProductName", as_index=False)
           .agg(Units=("Qty", "sum"), Revenue=("Revenue", "sum"))
           .nlargest(10, "Revenue"))

    trend = (orders[orders["Month"] <= month]
             .groupby("Month", as_index=False)["Revenue"].sum())
    trend["Month"] = trend["Month"].dt.strftime("%b %Y")

    unknown = int(this["ProductName"].isna().sum())
    return {"Summary": summary.round(1), "Reps": reps.round(1),
            "Top products": top.round(2), "Trend": trend.round(0),
            "unknown": unknown}

def add_trend_chart(wb, ws, n_months):
    """Add a native Excel line chart of the Trend sheet."""
    chart = wb.add_chart({"type": "line"})
    chart.add_series({
        "name": "Revenue",
        "categories": ["Trend", 3, 0, 2 + n_months, 0],
        "values": ["Trend", 3, 1, 2 + n_months, 1],
        "marker": {"type": "circle"},
    })
    chart.set_title({"name": "Revenue by month"})
    chart.set_legend({"none": True})
    ws.insert_chart("D3", chart)

def write_report(tables, month, out_dir=OUT):
    """Write a formatted Excel report and return its path."""
    out_dir.mkdir(exist_ok=True)
    path = out_dir / f"kestrel_report_{month}.xlsx"
    with pd.ExcelWriter(path, engine="xlsxwriter") as xw:
        wb = xw.book
        head = wb.add_format({"bold": True,
                              "bg_color": "#D9D9D9"})
        money = wb.add_format({"num_format": "$#,##0"})
        title = wb.add_format({"bold": True, "font_size": 14})

        for name in ["Summary", "Reps", "Top products", "Trend"]:
            df = tables[name]
            keep_index = name == "Summary"
            df.to_excel(xw, sheet_name=name, startrow=2,
                        index=keep_index)
            ws = xw.sheets[name]
            ws.write(0, 0, f"Kestrel Supplies: {name}, {month}",
                     title)
            cols = ([""] if keep_index else []) + list(df.columns)
            for c, label in enumerate(cols):
                ws.write(2, c, label, head)
            ws.set_column(0, 0, 28)
            ws.set_column(1, len(cols), 14)

        xw.sheets["Reps"].set_column("B:C", 14, money)
        xw.sheets["Top products"].set_column("C:C", 14, money)
        xw.sheets["Trend"].set_column("B:B", 14, money)
        add_trend_chart(wb, xw.sheets["Trend"],
                        len(tables["Trend"]))

        if tables["unknown"]:
            xw.sheets["Summary"].write(
                10, 0, f"Note: {tables['unknown']} order lines "
                "have an unknown product and no margin.")
    return path

def main():
    month = sys.argv[1] if len(sys.argv) > 1 else "2025-12"
    orders, targets = load_data()
    tables = build_tables(orders, targets, month)
    path = write_report(tables, month)
    print(f"Report written to {path}")


if __name__ == "__main__":
    main()
