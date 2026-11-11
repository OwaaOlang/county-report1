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
