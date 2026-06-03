from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

foods = ["Pizza", "Burger", "Biryani", "Pasta", "Dosa", "Idli"]

print("🚀 Order Producer Started...")

for order_id in range(1, 21):   # 🔥 sends 20 orders

    order = {
        "order_id": order_id,
        "customer": f"User_{order_id}",
        "food": random.choice(foods),
        "amount": random.randint(100, 800)
    }

    producer.send(
        "orders_v2",
        key=str(order_id).encode('utf-8'),   # 🔥 important for partitions
        value=order
    )

    print("Sent:", order)

    time.sleep(1)   # simulate real-time order flow

producer.flush()
print("✅ All orders sent successfully")