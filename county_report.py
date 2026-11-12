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

def list_counties():
    conn = sqlite3.connect("sales.db")
    df = pd.read_sql("SELECT DISTINCT county FROM orders", conn)
    conn.close()
    return df['county'].tolist()

def make_chart(df, county):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.bar(df['product'], df['total_revenue_kes'])
    plt.title(f"Revenue by Product - {county}")
    plt.xlabel("Product")
    plt.ylabel("Total Revenue (KES)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"Chart_{county}.png")
    plt.show()

def export_county_report_to_excel(county, start, end, filename):
    df = get_county_report(county, start, end)
    df.to_excel(filename, index=False)
    print(f"Saved Excel as {filename}")


if __name__ == "__main__":
    print("Available counties:", list_counties())
    county = input("Enter county from list above: ")
    start = input("Enter start date (YYYY-MM-DD): ")
    end = input("Enter end date (YYYY-MM-DD): ")

    df = get_county_report(county, start, end)

    if df.empty:
        print(f"No results for {county} from {start} to {end}")
    else:
        print(df)
        make_chart(df, county)
        export_county_report_to_excel(county, start, end, f"County_Report_{county}.xlsx")
        print("Done! Check your folder for chart and Excel.")
