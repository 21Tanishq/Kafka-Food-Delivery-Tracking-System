import sqlite3

conn = sqlite3.connect("food_delivery.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer TEXT,
    food TEXT,
    amount INTEGER
)
""")

conn.commit()
conn.close()

print("Orders table ready")