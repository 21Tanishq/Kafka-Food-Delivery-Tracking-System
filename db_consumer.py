from kafka import KafkaConsumer
import sqlite3
import json
from app import socketio, get_latest_data

consumer = KafkaConsumer(
    "delivery_updates_v2",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

conn = sqlite3.connect("food_delivery.db", check_same_thread=False)
cursor = conn.cursor()

print("DB Consumer Started...")

for msg in consumer:

    event = msg.value
    print("Received:", event)

    cursor.execute("""
        INSERT INTO order_events(order_id, status)
        VALUES (?, ?)
    """, (event["order_id"], event["delivery_status"]))

    conn.commit()

    # 🔥 REAL-TIME PUSH
    socketio.emit("update", get_latest_data())