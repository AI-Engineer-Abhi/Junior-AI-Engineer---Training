import sqlite3
import json

def init_db():
    conn = sqlite3.connect("shopeasy.db")
    cursor = conn.cursor()

    # 1. Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_name TEXT,
            status TEXT,
            items TEXT,
            total_amount REAL,
            shipping_address TEXT,
            carrier TEXT,
            tracking_number TEXT,
            estimated_delivery TEXT
        )
    """)

    # 2. Products Catalog Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL,
            stock INTEGER,
            rating REAL,
            description TEXT,
            icon TEXT
        )
    """)

    # 3. Store Policies Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS policies (
            category TEXT PRIMARY KEY,
            policy_text TEXT
        )
    """)

    # --- Clear existing data for fresh seed ---
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM products")
    cursor.execute("DELETE FROM policies")

    # --------------------------------------------------------------------------
    # 10 REALISTIC E-COMMERCE ORDERS
    # --------------------------------------------------------------------------
    orders_data = [
        ("ORD1234", "Sarah Jenkins", "Shipped", json.dumps(["ProSound Headphones", "Fast Charger 65W"]), 189.98, "742 Evergreen Terr, Springfield, IL", "FedEx", "FX-998234", "2026-08-06"),
        ("ORD5678", "Michael Scott", "Processing", json.dumps(["ErgoFlex Mesh Chair", "Desk Mat"]), 299.50, "1725 Slough Avenue, Scranton, PA", "UPS", "UPS-441209", "2026-08-08"),
        ("ORD9012", "Emma Watson", "Delivered", json.dumps(["FitPulse Smartwatch V2", "Leather Band"]), 349.00, "10 Downing St, London, UK", "DHL Express", "DHL-882101", "Delivered Aug 1, 2026"),
        ("ORD3344", "David Miller", "Out for Delivery", json.dumps(["VisionPro 27\" 4K Monitor"]), 399.00, "55 Wall Street, New York, NY", "USPS", "USPS-110293", "Today by 5:00 PM"),
        ("ORD7711", "Priya Sharma", "Processing", json.dumps(["RGB Mechanical Keyboard", "Gaming Mouse"]), 139.98, "102 Tech Park Way, Austin, TX", "BlueDart", "BD-771029", "2026-08-07"),
        ("ORD8822", "Alex Chen", "Delivered", json.dumps(["SonicBass Bluetooth Speaker"]), 79.95, "404 Silicon Ave, San Jose, CA", "Amazon Logistics", "TBA-992104", "Delivered Jul 29, 2026"),
        ("ORD4499", "Carlos Mendez", "Shipped", json.dumps(["UltraBook Pro 15\" Laptop"]), 1299.00, "88 Ocean Drive, Miami, FL", "FedEx", "FX-332910", "2026-08-05"),
        ("ORD6633", "Hannah Abbott", "On Hold", json.dumps(["Smart Ambient Desk Lamp", "Wireless Charger"]), 89.50, "12 Maple Street, Boston, MA", "UPS", "UPS-001293", "Pending Verification"),
        ("ORD2255", "Robert Downey", "Cancelled", json.dumps(["Precision Ergonomic Mouse"]), 49.99, "100 Malibu Point, Los Angeles, CA", "N/A", "N/A", "Order Cancelled"),
        ("ORD9900", "Sophia Taylor", "Refunded", json.dumps(["Studio Streamer USB Mic"]), 119.00, "250 Peachtree St, Atlanta, GA", "DHL", "DHL-440192", "Refund Issued Aug 2, 2026")
    ]
    cursor.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?)", orders_data)

    # --------------------------------------------------------------------------
    # 10 REALISTIC E-COMMERCE PRODUCTS
    # --------------------------------------------------------------------------
    products_data = [
            ("PROD-01", "ProSound Wireless Headphones", "Audio", 149.99, 24, 4.8, "Active noise-canceling with 30-hour battery life and quick charge.", "🎧"),
            ("PROD-02", "UltraBook Pro 15\"", "Laptops", 1299.00, 8, 4.9, "Intel i7, 16GB RAM, 512GB NVMe SSD ultra-slim aluminum body.", "💻"),
            ("PROD-03", "ErgoFlex Mesh Desk Chair", "Furniture", 249.50, 15, 4.6, "Breathable mesh back with adjustable 3D lumbar support.", "🪑"),
            ("PROD-04", "FitPulse Smartwatch V2", "Wearables", 199.00, 42, 4.7, "Real-time ECG, blood oxygen sensor, GPS, 50m waterproof OLED.", "⌚"),
            ("PROD-05", "RGB Mechanical Keyboard", "Gaming", 89.99, 0, 4.5, "Tactile switches with per-key customizable RGB illumination.", "⌨️"),
            ("PROD-06", "SonicBass Bluetooth Speaker", "Audio", 79.95, 30, 4.4, "360-degree surround sound with deep bass and IPX7 waterproofing.", "🔊"),
            ("PROD-07", "Precision Ergonomic Mouse", "Accessories", 49.99, 55, 4.8, "Dual wireless/Bluetooth modes with programmable shortcut thumb buttons.", "🖱️"),
            ("PROD-08", "VisionPro 27\" 4K Monitor", "Electronics", 399.00, 12, 4.9, "IPS panel, HDR400, 144Hz refresh rate with USB-C 65W power delivery.", "🖥️"),
            ("PROD-09", "Smart Ambient Desk Lamp", "Home", 39.99, 18, 4.3, "Color temperature tuning with built-in 10W Qi wireless charging pad.", "💡"),
            ("PROD-10", "Studio Streamer USB Mic", "Audio", 119.00, 5, 4.7, "Cardioid condenser microphone with hardware gain dial and pop filter.", "🎙️")
        ]
    cursor.executemany("INSERT INTO products VALUES (?,?,?,?,?,?,?,?)", products_data)

    # --------------------------------------------------------------------------
    # STORE POLICIES
    # --------------------------------------------------------------------------
    policies_data = [
        ("returns", "Returns are accepted within 30 days of delivery. Items must be unused and in original packaging. Return shipping is 100% free for store credit."),
        ("refunds", "Refunds are processed automatically to your original payment method within 3 to 5 business days after warehouse inspection."),
        ("shipping", "Standard Shipping takes 3-5 business days ($4.99, free on orders over $50). Express Shipping takes 1-2 business days ($14.99)."),
        ("payments", "We accept All major Credit/Debit Cards, Apple Pay, Google Pay, PayPal, Klarna Buy-Now-Pay-Later, and Cash on Delivery (COD).")
    ]
    cursor.executemany("INSERT INTO policies VALUES (?,?)", policies_data)

    conn.commit()
    conn.close()

# ------------------------------------------------------------------------------
# DATABASE HELPER FUNCTIONS & MUTATIONS
# ------------------------------------------------------------------------------
def query_order(order_id):
    conn = sqlite3.connect("shopeasy.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE UPPER(order_id) = UPPER(?)", (order_id.strip(),))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "order_id": row[0],
            "customer_name": row[1],
            "status": row[2],
            "items": json.loads(row[3]),
            "total": row[4],
            "address": row[5],
            "carrier": row[6],
            "tracking_number": row[7],
            "delivery": row[8]
        }
    return None

def fetch_all_orders():
    conn = sqlite3.connect("shopeasy.db")
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, customer_name, status, total_amount, carrier FROM orders")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_shipping_address(order_id, new_address):
    conn = sqlite3.connect("shopeasy.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET shipping_address = ? WHERE UPPER(order_id) = UPPER(?)", (new_address, order_id.strip()))
    modified = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return modified

def cancel_order_in_db(order_id):
    conn = sqlite3.connect("shopeasy.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'Cancelled' WHERE UPPER(order_id) = UPPER(?) AND status IN ('Processing', 'On Hold')", (order_id.strip(),))
    modified = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return modified

def search_products(query_term="", category="All", max_price=2000, in_stock_only=False):
    conn = sqlite3.connect("shopeasy.db")
    cursor = conn.cursor()
    
    sql = "SELECT * FROM products WHERE price <= ?"
    params = [max_price]

    if query_term:
        sql += " AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ?)"
        params.extend([f"%{query_term.lower()}%", f"%{query_term.lower()}%"])
        
    if category != "All":
        sql += " AND category = ?"
        params.append(category)

    if in_stock_only:
        sql += " AND stock > 0"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return [{
        "id": r[0], "name": r[1], "category": r[2], "price": r[3],
        "stock": r[4], "rating": r[5], "description": r[6], "icon": r[7]
    } for r in rows]

def get_policy(category):
    conn = sqlite3.connect("shopeasy.db")
    cursor = conn.cursor()
    cursor.execute("SELECT policy_text FROM policies WHERE category = ?", (category,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

if __name__ == "__main__":
    init_db()