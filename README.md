# Kafka Food Delivery Tracking System 
## Architecture

Order Producer
↓
orders_v2 topic with 3 partitions
↓
Delivery Consumers using Consumer Group
↓
delivery_updates_v2
↓
DB Consumer → SQLite → Flask Dashboard
↓
Notification Service → notifications topic → Notification Consumer

Failed messages are routed to:

orders_v2
↓
Dead Letter Queue
↓
dead_letter_orders

## Dashboard Preview

![Dashboard](d:\kafka project2\screenshots\Screenshot (142).png)
![Dashboard](d:\kafka project2\screenshots\Screenshot (143).png)
![Dashboard](d:\kafka project2\screenshots\Screenshot (144).png)
![Dashboard](d:\kafka project2\screenshots\Screenshot (145).png)

