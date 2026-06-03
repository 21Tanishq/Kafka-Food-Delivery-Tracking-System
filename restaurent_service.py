from kafka import KafkaConsumer, KafkaProducer
import json
import time

consumer = KafkaConsumer(
    "payments",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for msg in consumer:

    payment = msg.value

    if payment["payment_status"] == "SUCCESS":

        order_id = payment["order_id"]

        statuses = [
            "PREPARING",
            "READY"
        ]

        for status in statuses:

            update = {
                "order_id": order_id,
                "restaurant_status": status
            }

            producer.send("restaurant_updates", update)
            producer.flush()

            print(update)

            time.sleep(5)