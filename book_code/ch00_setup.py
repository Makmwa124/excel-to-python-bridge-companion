"""Chapter 0: Set up in fifteen minutes

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd

orders = pd.read_excel("data/kestrel_sales.xlsx",
                       sheet_name="Orders")
orders.shape

