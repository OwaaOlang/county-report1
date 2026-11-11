import sqlite3
import pandas as pd

def get_county_report(county, start_date, end_date):
    conn = sqlite3.connect("sales.db")
    query = """
    SELECT product,
           COUNT(*) AS total_orders,
           SUM(quantity) AS total_quantity,
           SUM(total_value) AS total_revenue_kes
    FROM orders
    WHERE county = ? AND order_date BETWEEN ? AND ?
    GROUP BY product
    ORDER BY total_revenue_kes DESC
    """
    df = pd.read_sql_query(query, conn, params=(county, start_date, end_date))
    conn.close()
    if df.empty:
        print(f"No results for {county} from {start_date} to {end_date}")
    return df

print(get_county_report("Nairobi", "2024-01-01", "2024-01-31"))
print(get_county_report("Kisumu", "2024-02-01", "2024-02-29"))
print(get_county_report("Mombasa", "2024-01-01", "2024-02-29"))
print(get_county_report("Nairobi", "2024-03-01", "2024-03-31"))

import matplotlib.pyplot as plt

def get_total_revenue(start_date, end_date):
    conn = sqlite3.connect("sales.db")
    query = """
    SELECT SUM(total_value) AS total_revenue
    FROM orders
    WHERE order_date BETWEEN ? AND ?
    """
    df = pd.read_sql_query(query, conn, params=(start_date, end_date))
    conn.close()
    return df.iloc[0, 0] or 0

def plot_top_products(start_date, end_date):
    conn = sqlite3.connect("sales.db")
    query = """
    SELECT product, SUM(total_value) AS revenue
    FROM orders
    WHERE order_date BETWEEN ? AND ?
    GROUP BY product
    ORDER BY revenue DESC
    """
    df = pd.read_sql_query(query, conn, params=(start_date, end_date))
    conn.close()

    plt.bar(df['product'], df['revenue'])
    plt.title(f"Top Products {start_date} to {end_date}")
    plt.ylabel("Revenue KES")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("top_products.png", dpi=150)
    plt.show()
    print("Saved as top_products.png")

print("Total Jan-Feb:", get_total_revenue("2024-01-01", "2024-02-29"))
plot_top_products("2024-01-01", "2024-02-29")
