from kafka import KafkaConsumer, KafkaProducer
import json
import time

consumer = KafkaConsumer(
    "restaurant_updates",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Delivery Service Started...")

for msg in consumer:

    restaurant_event = msg.value

    print("Received:", restaurant_event)

    if restaurant_event["restaurant_status"] == "READY":

        order_id = restaurant_event["order_id"]

        delivery_events = [
            "PICKED_UP",
            "OUT_FOR_DELIVERY",
            "DELIVERED"
        ]

        for status in delivery_events:

            event = {
                "order_id": order_id,
                "delivery_status": status
            }

            producer.send(
    "delivery_updates",
    key=str(order_id).encode("utf-8"),   # 🔥 THIS decides partition
    value=event
)
            producer.flush()

            print("Sent:", event)

            time.sleep(5)