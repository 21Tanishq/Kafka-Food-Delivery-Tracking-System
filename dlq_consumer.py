from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "dead_letter_orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("DLQ Consumer Started...")

for msg in consumer:
    print("\nBAD MESSAGE FOUND")
    print(msg.value)