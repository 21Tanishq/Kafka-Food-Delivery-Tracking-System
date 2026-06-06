from kafka import KafkaConsumer, KafkaProducer
import json

consumer = KafkaConsumer(
    "retry_orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Retry Consumer Started...")

for msg in consumer:

    retry_data = msg.value

    payload = retry_data["payload"]

    retry_count = retry_data["retry_count"]

    print(
        f"Retry Attempt {retry_count}",
        payload
    )

    try:

        required = [
            "order_id",
            "customer",
            "food",
            "amount"
        ]

        for field in required:

            if field not in payload:

                raise Exception(
                    f"Missing {field}"
                )

        print(
            "Recovered Successfully"
        )

    except Exception as e:

        if retry_count < 3:

            retry_data["retry_count"] += 1

            producer.send(
                "retry_orders",
                retry_data
            )

            producer.flush()

            print(
                f"Requeued Retry {retry_count+1}"
            )

        else:

            producer.send(
                "dead_letter_orders",
                {
                    "error": str(e),
                    "payload": payload
                }
            )

            producer.flush()

            print(
                "Moved To DLQ"
            )