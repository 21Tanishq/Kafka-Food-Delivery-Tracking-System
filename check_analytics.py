import sqlite3

conn = sqlite3.connect("food_delivery.db")
cursor = conn.cursor()

print("\nORDERS TABLE:\n")

cursor.execute("SELECT * FROM orders LIMIT 10")

for row in cursor.fetchall():
    print(row)

print("\nREVENUE:\n")

cursor.execute("SELECT SUM(amount) FROM orders")
print(cursor.fetchone())

print("\nTOP FOOD:\n")

cursor.execute("""
SELECT food, COUNT(*)
FROM orders
GROUP BY food
ORDER BY COUNT(*) DESC
LIMIT 1
""")

print(cursor.fetchone())

conn.close()