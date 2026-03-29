"""
database.py  —  MySQL version for SuperMart (Fixed)
Password already set to: root
"""

import mysql.connector
from mysql.connector import Error

# ── ⚙️  DATABASE SETTINGS ─────────────────────────────────────────────────────
DB_CONFIG = {
    "host":             "localhost",
    "port":             3306,
    "user":             "root",
    "password":         "root",           # ← Your MySQL password
    "database":         "supermarket_db",
    "consume_results":  True,             # ← Fixes the "Unread result" error
}
# ─────────────────────────────────────────────────────────────────────────────


def get_connection():
    """Return a live MySQL connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise RuntimeError(
            f"Cannot connect to MySQL.\n\n"
            f"Error: {e}\n\n"
            f"Please check:\n"
            f"  1. MySQL Server is running\n"
            f"  2. Password in database.py matches your MySQL root password\n"
            f"  3. The database 'supermarket_db' exists in MySQL Workbench"
        )


def _execute(query, params=(), fetch=None, many=False):
    """Internal helper — runs a query and optionally fetches results."""
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    result = None
    try:
        if many:
            cur.executemany(query, params)
        else:
            cur.execute(query, params)

        if fetch == "one":
            result = cur.fetchone()
        elif fetch == "all":
            result = cur.fetchall()
        else:
            result = cur.lastrowid

        conn.commit()
        return result
    except Error as e:
        conn.rollback()
        raise e
    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


# ── Create tables ─────────────────────────────────────────────────────────────

def initialize_db():
    """Create all tables and seed default data."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role     ENUM('admin','user') NOT NULL DEFAULT 'user'
        )
    """)
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id    INT AUTO_INCREMENT PRIMARY KEY,
            name  VARCHAR(200) UNIQUE NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            stock INT NOT NULL DEFAULT 0
        )
    """)
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id             INT AUTO_INCREMENT PRIMARY KEY,
            bill_id        VARCHAR(50)   NOT NULL,
            customer_name  VARCHAR(200),
            customer_phone VARCHAR(20),
            product_name   VARCHAR(200)  NOT NULL,
            quantity       INT           NOT NULL,
            unit_price     DECIMAL(10,2) NOT NULL,
            total          DECIMAL(10,2) NOT NULL,
            payment_method VARCHAR(50),
            date           DATETIME      NOT NULL
        )
    """)
    conn.commit()

    # Default admin
    cur.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    row = cur.fetchone()
    if row[0] == 0:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            ("admin", "admin123", "admin")
        )
        conn.commit()

    # Sample products
    cur.execute("SELECT COUNT(*) FROM products")
    row = cur.fetchone()
    if row[0] == 0:
        sample_products = [
            ("Rice (1kg)",        55.00, 100),
            ("Wheat Flour (1kg)", 45.00,  80),
            ("Sugar (1kg)",       42.00, 120),
            ("Salt (1kg)",        18.00, 200),
            ("Cooking Oil (1L)", 130.00,  60),
            ("Milk (500ml)",      28.00,  90),
            ("Bread",             35.00,  50),
            ("Eggs (12pcs)",      72.00,  40),
            ("Butter (100g)",     55.00,  35),
            ("Tea Powder (250g)", 85.00,  45),
        ]
        cur.executemany(
            "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
            sample_products
        )
        conn.commit()

    cur.close()
    conn.close()


# ── User queries ──────────────────────────────────────────────────────────────

def get_user(username, password):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def add_user(username, password, role="user"):
    try:
        _execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, role)
        )
        return True
    except Error:
        return False


def get_all_users():
    return _execute(
        "SELECT id, username, role FROM users",
        fetch="all"
    ) or []


def delete_user(user_id):
    _execute("DELETE FROM users WHERE id=%s", (user_id,))


# ── Product queries ───────────────────────────────────────────────────────────

def get_all_products():
    return _execute(
        "SELECT * FROM products ORDER BY name",
        fetch="all"
    ) or []


def get_product_by_name(name):
    return _execute(
        "SELECT * FROM products WHERE name=%s",
        (name,), fetch="one"
    )


def add_product(name, price, stock):
    try:
        _execute(
            "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
            (name, price, stock)
        )
        return True, "Product added successfully."
    except Error:
        return False, "Product with this name already exists."


def update_product(product_id, name, price, stock):
    try:
        _execute(
            "UPDATE products SET name=%s, price=%s, stock=%s WHERE id=%s",
            (name, price, stock, product_id)
        )
        return True, "Product updated successfully."
    except Error:
        return False, "Product name already exists."


def delete_product(product_id):
    _execute("DELETE FROM products WHERE id=%s", (product_id,))


def reduce_stock(product_name, quantity):
    _execute(
        "UPDATE products SET stock = stock - %s WHERE name=%s",
        (quantity, product_name)
    )


# ── Sales queries ─────────────────────────────────────────────────────────────

def save_sale(bill_id, customer_name, customer_phone, items, payment_method, date):
    conn = get_connection()
    cur = conn.cursor()
    for item in items:
        cur.execute("""
            INSERT INTO sales
              (bill_id, customer_name, customer_phone, product_name,
               quantity, unit_price, total, payment_method, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            bill_id, customer_name, customer_phone,
            item["name"], item["qty"], item["price"],
            item["qty"] * item["price"], payment_method, date
        ))
    conn.commit()
    cur.close()
    conn.close()


def get_sales_summary():
    return _execute("""
        SELECT DATE_FORMAT(date, '%Y-%m') AS month,
               SUM(total)                AS revenue,
               COUNT(DISTINCT bill_id)   AS bills
        FROM sales
        GROUP BY month
        ORDER BY month DESC
    """, fetch="all") or []


def get_all_sales():
    return _execute(
        "SELECT * FROM sales ORDER BY date DESC",
        fetch="all"
    ) or []


def get_today_revenue():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT COALESCE(SUM(total), 0) AS rev
        FROM sales
        WHERE DATE(date) = CURDATE()
    """)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return float(row["rev"]) if row else 0.0


def get_total_revenue():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COALESCE(SUM(total), 0) AS rev FROM sales")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return float(row["rev"]) if row else 0.0
