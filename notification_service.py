from kafka import KafkaConsumer, KafkaProducer
import json

consumer = KafkaConsumer(
    "delivery_updates_v2",
    bootstrap_servers="localhost:9092",
    group_id="notification_group_debug",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Notification Service Started... Waiting for delivery events")

for msg in consumer:
    event = msg.value

    print("Received delivery event:", event)

    status = event.get("delivery_status")
    order_id = event.get("order_id")

    print("Status received:", status)

    if status == "DELIVERED":
        notification = {
            "order_id": order_id,
            "message": f"Your order #{order_id} has been delivered.",
            "type": "ORDER_DELIVERED"
        }

        producer.send("notifications", notification)
        producer.flush()

        print("Notification Created:", notification)