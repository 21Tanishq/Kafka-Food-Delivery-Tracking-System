import sqlite3

conn = sqlite3.connect("food_delivery.db")
cursor = conn.cursor()

try:
    cursor.execute(
        "ALTER TABLE order_events ADD COLUMN food TEXT"
    )
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE order_events ADD COLUMN amount INTEGER"
    )
except:
    pass

conn.commit()
conn.close()

print("Database upgraded successfully")