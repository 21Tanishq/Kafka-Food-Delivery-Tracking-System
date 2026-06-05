from kafka import KafkaConsumer, KafkaProducer
import json
import time

consumer = KafkaConsumer(
    "orders_v2",
    bootstrap_servers="localhost:9092",
    group_id="delivery_group",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Delivery Consumer Started...")

for msg in consumer:
    order = msg.value

    print("Received Order:", order)

    order_id = order["order_id"]

    statuses = [
        "PICKED_UP",
        "OUT_FOR_DELIVERY",
        "DELIVERED"
    ]

    for status in statuses:
        event = {
            "order_id": order_id,
            "delivery_status": status
        }

        producer.send(
            "delivery_updates_v2",
            key=str(order_id).encode("utf-8"),
            value=event
        )

        producer.flush()

        print("Sent Delivery Update:", event)

        time.sleep(2)