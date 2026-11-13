import sqlite3
import pandas as pd

DB_FILE = "sales.db"

def get_conn():
    return sqlite3.connect(DB_FILE)

# Q1: In YOUR data, delivered = completed, pending = pending, cancelled = 0
q1 = """
SELECT 
    county,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(CASE WHEN status = 'delivered' THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id), 1) AS pct_completed,
    ROUND(SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id), 1) AS pct_pending,
    ROUND(SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id), 1) AS pct_cancelled
FROM orders
GROUP BY county
ORDER BY county;
"""
# BUSINESS INTERPRETATION 1: Counties with high pending % need delivery follow-up to convert to delivered, while 0% cancelled shows strong fulfillment in this sample.

# Q2: Uses 'delivered' not 'completed'
q2 = """
WITH monthly_sales AS (
    SELECT 
        customer,
        strftime('%Y-%m', order_date) AS month,
        SUM(total_value) AS monthly_value
    FROM orders
    WHERE status = 'delivered'
    GROUP BY customer, strftime('%Y-%m', order_date)
),
with_lag AS (
    SELECT 
        customer,
        month,
        monthly_value,
        LAG(monthly_value, 1) OVER (PARTITION BY customer ORDER BY month) AS prev_month,
        LAG(monthly_value, 2) OVER (PARTITION BY customer ORDER BY month) AS prev_2_month
    FROM monthly_sales
),
growth_flag AS (
    SELECT *,
        CASE WHEN monthly_value > prev_month THEN 1 ELSE 0 END AS is_growth,
        CASE WHEN prev_month > prev_2_month THEN 1 ELSE 0 END AS prev_is_growth
    FROM with_lag
)
SELECT DISTINCT customer
FROM growth_flag
WHERE is_growth = 1 AND prev_is_growth = 1
ORDER BY customer;
"""
# BUSINESS INTERPRETATION 2: These customers show sustained momentum for two consecutive months and are prime candidates for loyalty rewards or upsell offers before momentum fades.

# Q3: Uses 'delivered'
q3 = """
WITH daily_revenue AS (
    SELECT 
        DATE(order_date) AS order_day,
        SUM(total_value) AS daily_revenue
    FROM orders
    WHERE status = 'delivered'
    GROUP BY DATE(order_date)
)
SELECT 
    order_day,
    daily_revenue,
    SUM(daily_revenue) OVER (ORDER BY order_day) AS running_total_revenue
FROM daily_revenue
ORDER BY order_day;
"""
# BUSINESS INTERPRETATION 3: The running total curve shows whether overall revenue growth is accelerating or flattening over time, helping the board spot cashflow inflection points early.

def run():
    conn = get_conn()
    print("\n=== Q1: % Delivered / Pending / Cancelled per County ===")
    df1 = pd.read_sql_query(q1, conn)
    print(df1.to_string(index=False))
    print("\n=== Q2: Customers with 2 consecutive months growth (LAG) ===")
    df2 = pd.read_sql_query(q2, conn)
    print(df2.to_string(index=False))
    print(f"Total: {len(df2)} customers")
    print("\n=== Q3: Running Total Revenue by Date ===")
    df3 = pd.read_sql_query(q3, conn)
    print(df3.to_string(index=False))
    conn.close()

if __name__ == "__main__":
    run()
