from kafka import KafkaConsumer, KafkaProducer
import json
import time

consumer = KafkaConsumer(
    "restaurant_updates",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for msg in consumer:

    update = msg.value

    if update["restaurant_status"] == "READY":

        order_id = update["order_id"]

        delivery_statuses = [
            "PICKED_UP",
            "OUT_FOR_DELIVERY",
            "DELIVERED"
        ]

        for status in delivery_statuses:

            event = {
                "order_id": order_id,
                "delivery_status": status
            }

            producer.send("delivery_updates", event)
            producer.flush()

            print(event)

            time.sleep(5)