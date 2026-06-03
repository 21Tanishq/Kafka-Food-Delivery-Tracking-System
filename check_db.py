import sqlite3

conn = sqlite3.connect("food_delivery.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(order_events)")
print("TABLE STRUCTURE:")
print(cursor.fetchall())

cursor.execute("SELECT * FROM order_events LIMIT 5")
print("\nSAMPLE DATA:")
print(cursor.fetchall())

conn.close()