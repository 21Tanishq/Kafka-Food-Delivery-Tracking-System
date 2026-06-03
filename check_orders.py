import sqlite3

conn = sqlite3.connect("food_delivery.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM orders")

for row in cursor.fetchall():
    print(row)

conn.close()