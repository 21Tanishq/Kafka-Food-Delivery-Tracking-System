from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "order_status",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m:
        json.loads(m.decode('utf-8'))
)

for msg in consumer:
    print(msg.value)