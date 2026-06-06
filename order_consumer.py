from kafka import KafkaConsumer, KafkaProducer
import sqlite3
import json

consumer = KafkaConsumer(
    "orders_v2",
    bootstrap_servers="localhost:9092",
    group_id="order_group",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

conn = sqlite3.connect("food_delivery.db", check_same_thread=False)
cursor = conn.cursor()

print("Order Consumer Started...")

for msg in consumer:

    try:
        order = msg.value

        required_fields = [
            "order_id",
            "customer",
            "food",
            "amount"
        ]

        for field in required_fields:
            if field not in order:
                raise ValueError(f"Missing field: {field}")

        cursor.execute("""
            INSERT OR REPLACE INTO orders
            (order_id, customer, food, amount)
            VALUES (?, ?, ?, ?)
        """, (
            order["order_id"],
            order["customer"],
            order["food"],
            order["amount"]
        ))

        conn.commit()

        print("Processed:", order)

    except Exception as e:

        retry_message = {
            "retry_count": 1,
            "error": str(e),
            "topic": msg.topic,
            "partition": msg.partition,
            "offset": msg.offset,
            "payload": msg.value
        }

        producer.send(
            "retry_orders",
            retry_message
        )

        producer.flush()

        print("Sent to Retry Queue:", retry_message)