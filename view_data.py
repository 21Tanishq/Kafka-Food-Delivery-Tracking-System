import sqlite3
import os

print(os.path.abspath("food_delivery.db"))

conn = sqlite3.connect("food_delivery.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM order_events"
)

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
input("Press Enter to exit...")