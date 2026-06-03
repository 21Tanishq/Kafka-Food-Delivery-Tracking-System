from kafka import KafkaConsumer
import json
consumer = KafkaConsumer(
    "orders",   # 🔥 must match producer
    bootstrap_servers="localhost:9092",
    group_id="delivery_group",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Delivery Consumer 2 Started...")

for msg in consumer:
    print("Consumer 2:", msg.value)