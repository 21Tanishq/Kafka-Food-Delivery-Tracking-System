from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

notification = {
    "order_id": 999,
    "message": "Test notification",
    "type": "TEST"
}

producer.send("notifications", notification)
producer.flush()

print("Test notification sent")