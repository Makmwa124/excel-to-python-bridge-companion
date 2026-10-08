"""Chapter 8: Cleaning a messy sheet

Code from The Excel-to-Python Bridge by Mathew Kariuki.
Run from the companion folder, or paste into a notebook cell by cell.
"""

# --- Step 1 ---
import pandas as pd
import numpy as np

raw = pd.read_excel("data/customer_export_messy.xlsx")
raw.shape

# --- Step 2 ---
raw.isna().sum()

# --- Step 3 ---
raw["State"].value_counts()

# --- Step 4 ---
raw["Segment"].value_counts()

# --- Step 5 ---
df = raw.copy()

# --- Step 6 ---
print(df["CustomerName"].str.len().head(3).tolist())
df["CustomerName"] = (df["CustomerName"]
                      .str.strip()
                      .str.replace(r"\s+", " ", regex=True))
print(df["CustomerName"].str.len().head(3).tolist())

# --- Step 7 ---
text_cols = df.select_dtypes("str").columns
df[text_cols] = df[text_cols].apply(lambda s: s.str.strip())

# --- Step 8 ---
df["CustomerName"] = df["CustomerName"].str.title()
df.loc[[4, 21, 42], "CustomerName"]

# --- Step 9 ---
state_fix = {"SOUTH AUSTRALIA": "SA"}
df["State"] = df["State"].str.upper().replace(state_fix)
df["State"].value_counts()

# --- Step 10 ---
df["Segment"] = (df["Segment"].str.title()
                 .replace({"Café": "Cafe"}))
df["Segment"].value_counts()

# --- Step 11 ---
df["CreditLimit"].unique().tolist()

# --- Step 12 ---
df["CreditLimit"] = pd.to_numeric(
    df["CreditLimit"].astype(str).str.replace(",", ""),
    errors="coerce")
df["CreditLimit"].describe()[["count", "min", "max"]]

# --- Step 13 ---
df["JoinDate"].iloc[[10, 11, 24]].tolist()

# --- Step 14 ---
d1 = pd.to_datetime(df["JoinDate"], format="%d/%m/%Y",
                    errors="coerce")
d2 = pd.to_datetime(df["JoinDate"], format="%Y-%m-%d",
                    errors="coerce")
df["JoinDate"] = d1.fillna(d2)
df["JoinDate"].iloc[[10, 11, 24]]

# --- Step 15 ---
digits = df["Phone"].str.replace(r"\D", "", regex=True)
digits = digits.str.replace(r"^61", "0", regex=True)
df["Phone"] = (digits.str[:2] + " " + digits.str[2:6]
               + " " + digits.str[6:])
df["Phone"].iloc[[5, 26, 39]].tolist()

# --- Step 16 ---
dupes = df[df.duplicated("CustomerID", keep=False)]
dupes.sort_values("CustomerID")[["CustomerID",
                                  "CustomerName"]]

# --- Step 17 ---
before = len(df)
df = df.drop_duplicates(subset="CustomerID", keep="first")
before, len(df)

# --- Step 18 ---
df["CreditLimit"] = df["CreditLimit"].fillna(2000).astype(int)
df.isna().sum()[lambda s: s > 0]

# --- Step 19 ---
df.info()

# --- Step 20 ---
assert df["CustomerID"].is_unique
assert df["State"].isin(["SA", "VIC", "NSW", "WA"]).all()
assert (df["CreditLimit"] > 0).all()
print("All checks passed")

