from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "payments",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for msg in consumer:
    print(msg.value)