from kafka import KafkaConsumer, KafkaProducer
import json
import random

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for msg in consumer:

    order = msg.value

    payment = {
        "order_id": order["order_id"],
        "payment_status": random.choice(
            ["SUCCESS", "FAILED"]
        )
    }

    producer.send("payments", payment)
    producer.flush()

    print(payment)