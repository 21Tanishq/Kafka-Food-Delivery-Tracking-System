from kafka.admin import KafkaAdminClient, NewTopic

admin = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
    client_id="topic_admin"
)

topics = admin.list_topics()
print("Existing topics:", topics)

new_topics = [
    NewTopic(name="orders_v2", num_partitions=3, replication_factor=1),
    NewTopic(name="delivery_updates_v2", num_partitions=3, replication_factor=1),
    NewTopic(name="dead_letter_orders", num_partitions=1, replication_factor=1)
]

try:
    admin.create_topics(new_topics=new_topics, validate_only=False)
    print("Topics created successfully")
except Exception as e:
    print("Create topic error:", e)

print("Updated topics:", admin.list_topics())

admin.close()