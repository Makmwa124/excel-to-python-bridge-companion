# The Excel-to-Python Bridge: companion files

Free practice files for the book **The Excel-to-Python Bridge: Every Spreadsheet Task You Already Know, Translated into pandas Side by Side** by Mathew Kariuki.

Every example in the book uses Kestrel Supplies, a fictional business, and its sales workbook. This repository holds that workbook, the same data as CSV files, and every code example from the book, so you can follow along.

## Download

Click the green **Code** button above, then **Download ZIP**. Unzip it somewhere sensible, such as your Documents folder.

## What's here

| Path | What it is |
| --- | --- |
| `data/kestrel_sales.xlsx` | The practice workbook (Orders, Customers, Products, Targets, Freight) |
| `data/orders.csv`, `customers.csv`, `products.csv` | The same tables as CSV files |
| `data/product_report.xlsx` | An awkward report layout (Chapter 1) |
| `data/customer_export_messy.xlsx` | A messy CRM export (Chapter 8) |
| `data/monthly/` | Three monthly order exports to stack (Chapter 9) |
| `book_code/` | Every code example, chapter by chapter, as `.py` files |
| `scripts/monthly_report.py` | The automated monthly report from Chapter 13 |

## Quick start

1. Install Python, then run:

   ```
   pip install pandas openpyxl xlsxwriter matplotlib pyarrow jupyter
   ```

2. In VS Code, choose **File > Open Folder** and open this folder.
3. Create a notebook here (**File > New File > Jupyter Notebook**) and run:

   ```python
   import pandas as pd
   orders = pd.read_excel("data/kestrel_sales.xlsx", sheet_name="Orders")
   orders.head()
   ```

Paths such as `data/kestrel_sales.xlsx` assume this folder is your working directory. Examples that write files save them to an `output` folder.

Tested with Python 3.13 and pandas 3.0.

## Get the book

- **Paperback:** [Amazon.com](https://www.amazon.com/dp/B0HMNPS9BT) · [Amazon.com.au](https://www.amazon.com.au/dp/B0HMNPS9BT)
- **Kindle:** [Amazon.com](https://www.amazon.com/dp/B0HMNMJZ11) · [Amazon.com.au](https://www.amazon.com.au/dp/B0HMNMJZ11)

## About

Kestrel Supplies and every person and business in its data are fictional. The data and code are free to use for learning. The book itself is © 2026 Mathew Kariuki.

Spotted a problem with an example or the data? Please open an issue.
