"""Chapter 11: Conditional formatting and charts

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd
import matplotlib.pyplot as plt

xl = "data/kestrel_sales.xlsx"
orders = pd.read_excel(xl, sheet_name="Orders")
products = pd.read_excel(xl, sheet_name="Products")
orders["Revenue"] = (orders["Qty"] * orders["UnitPrice"]
                     * (1 - orders["Discount"])).round(2)
orders = orders.merge(products[["ProductCode", "Category"]],
                      on="ProductCode", how="left")
orders["Month"] = orders["OrderDate"].dt.strftime("%m-%b")

pt = orders.pivot_table(index="Category", columns="Rep",
                        values="Revenue", aggfunc="sum")
pt.columns = [name.split()[0] for name in pt.columns]

# --- Step 2 ---
pt.style.format("${:,.0f}")

# --- Step 3 ---
(pt.style
   .format("${:,.0f}")
   .background_gradient(cmap="Greys", axis=None)
   .highlight_max(axis=1, props="font-weight: bold"))

# --- Step 4 ---
cat = (orders.groupby("Category")["Revenue"].sum()
       .sort_values(ascending=False).to_frame())
cat.style.format("${:,.0f}").bar(color="#bbbbbb", width=90)

# --- Step 5 ---
def flag_low(v):
    if v < 5000:
        return "color: white; background-color: #444"
    return ""

pt.style.format("${:,.0f}").map(flag_low)

# --- Step 6 ---
monthly = orders.groupby("Month")["Revenue"].sum()
ax = monthly.plot(color="black", marker="o", figsize=(6, 3))
ax.set_title("Kestrel Supplies revenue by month, 2025")
ax.set_xlabel("")
ax.set_ylabel("Revenue ($)")
plt.show()

# --- Step 7 ---
by_cat = (orders.groupby("Category")["Revenue"].sum()
          .sort_values() / 1000)
fig, ax = plt.subplots(figsize=(6, 3))
by_cat.plot.barh(ax=ax, color="#555555")
ax.set_title("Revenue by category, 2025 ($ thousands)")
ax.set_ylabel("")
for side in ["top", "right"]:
    ax.spines[side].set_visible(False)
for i, v in enumerate(by_cat):
    ax.text(v + 2, i, f"{v:,.0f}", va="center")
plt.show()

# --- Step 8 ---
targets = pd.read_excel(xl, sheet_name="Targets")
tgt = targets.drop(columns="Rep").sum()
month_num = orders["OrderDate"].dt.month
act = orders.groupby(month_num)["Revenue"].sum()

fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(tgt.index, act.values / 1000, color="#999999",
       label="Actual")
ax.plot(tgt.index, tgt.values / 1000, color="black",
        marker="o", label="Target")
ax.set_title("Actual vs target, all reps ($ thousands)")
ax.legend(frameon=False, loc="upper left")
plt.show()

# --- Step 9 ---
ax = by_cat.plot.barh(color="#555555", figsize=(6, 3))
plt.savefig("revenue_by_category.png", dpi=200,
            bbox_inches="tight")
plt.close()

