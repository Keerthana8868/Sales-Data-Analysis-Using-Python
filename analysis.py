"""
Sales Data Analysis and Visualization
Run: python analysis.py
The script reads data/sales_data.csv and saves charts and summary tables in outputs/.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "sales_data.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Load data
df = pd.read_csv(DATA_FILE)
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

# 2. Clean data
df = df.drop_duplicates()
df = df.dropna(subset=["Order_Date", "Product", "Quantity", "Unit_Price"])
df["Sales"] = df["Quantity"] * df["Unit_Price"]
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)

# 3. Key performance indicators
total_revenue = df["Sales"].sum()
total_orders = df["Order_ID"].nunique()
total_units = df["Quantity"].sum()
average_order_value = total_revenue / total_orders if total_orders else 0

print("\n========== SALES ANALYSIS SUMMARY ==========")
print(f"Total revenue       : Rs. {total_revenue:,.2f}")
print(f"Total orders        : {total_orders}")
print(f"Units sold          : {total_units}")
print(f"Average order value : Rs. {average_order_value:,.2f}")

# 4. Product and category analysis
product_sales = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
city_sales = df.groupby("City")["Sales"].sum().sort_values(ascending=False)
monthly_sales = df.groupby("Month")["Sales"].sum().sort_index()

print("\nTop 5 products by revenue:")
print(product_sales.head(5).to_string())
print("\nRevenue by category:")
print(category_sales.to_string())
print("\nRevenue by city:")
print(city_sales.to_string())

# 5. Save summary tables
product_sales.to_csv(OUTPUT_DIR / "product_sales.csv", header=["Revenue"])
category_sales.to_csv(OUTPUT_DIR / "category_sales.csv", header=["Revenue"])
monthly_sales.to_csv(OUTPUT_DIR / "monthly_sales.csv", header=["Revenue"])
city_sales.to_csv(OUTPUT_DIR / "city_sales.csv", header=["Revenue"])

# 6. Create charts
plt.figure(figsize=(9, 5))
product_sales.plot(kind="bar", title="Revenue by Product")
plt.ylabel("Revenue (Rs.)")
plt.xlabel("Product")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_product.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
category_sales.plot(kind="bar", title="Revenue by Category")
plt.ylabel("Revenue (Rs.)")
plt.xlabel("Category")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_category.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 5))
monthly_sales.plot(kind="line", marker="o", title="Monthly Revenue Trend")
plt.ylabel("Revenue (Rs.)")
plt.xlabel("Month")
plt.xticks(rotation=45, ha="right")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_revenue_trend.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
city_sales.plot(kind="bar", title="Revenue by City")
plt.ylabel("Revenue (Rs.)")
plt.xlabel("City")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_city.png", dpi=150)
plt.close()

print(f"\nAnalysis completed. Charts and CSV summaries are saved in: {OUTPUT_DIR}")
