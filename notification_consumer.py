from kafka import KafkaConsumer
import json
import sqlite3

consumer = KafkaConsumer(
    "notifications",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

conn = sqlite3.connect("food_delivery.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    message TEXT,
    type TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

print("Notification Consumer Started...")

for msg in consumer:
    notification = msg.value

    cursor.execute("""
        INSERT INTO notifications(order_id, message, type)
        VALUES (?, ?, ?)
    """, (
        notification["order_id"],
        notification["message"],
        notification["type"]
    ))

    conn.commit()

    print("\n📱 Notification Sent")
    print("Order ID:", notification["order_id"])
    print("Message:", notification["message"])