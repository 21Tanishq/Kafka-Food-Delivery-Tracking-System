import sqlite3

conn = sqlite3.connect("food_delivery.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    status TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database created successfully")