from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "orders_v2",   # 🔥 must match producer
    bootstrap_servers="localhost:9092",
    group_id="delivery_group",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Delivery Consumer Started...")
for msg in consumer:
    print(
        f"Partition {msg.partition} | Key {msg.key} | Value {msg.value}"
    )