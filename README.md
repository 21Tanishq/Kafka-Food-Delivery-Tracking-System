# Kafka Food Delivery Tracking System

A real-time food delivery tracking platform built using Apache Kafka, Python, Flask, SocketIO, and SQLite. The system simulates a production-style food delivery workflow with event-driven microservices, partition-based scaling, retry mechanisms, dead-letter queues, and live monitoring dashboards.

---

## Features

### Core Kafka Features

* Kafka Producers and Consumers
* Consumer Groups
* Multi-Partition Topics
* Partition-Based Scaling
* Event-Driven Architecture

### Reliability Features

* Retry Queue
* Dead Letter Queue (DLQ)
* Fault Tolerance
* Error Handling

### Real-Time Tracking

* Live Order Tracking
* Delivery Status Updates
* Delivery Agent Tracking
* Real-Time Notifications

### Dashboard & Analytics

* Flask Dashboard
* SocketIO Real-Time Updates
* Revenue Analytics
* Top Food Analytics
* Order Monitoring
* Notification Monitoring
* System Statistics Dashboard

---

## Architecture

Order Producer
↓
orders_v2 (3 Partitions)
↓
Order Consumer Group
↓
Valid Orders → Database

Invalid Orders
↓
retry_orders
↓
Retry Consumer
↓
Success OR DLQ

Database
↓
Delivery Service
↓
delivery_updates_v2
↓
DB Consumer

delivery_updates_v2
↓
Notification Service
↓
notifications
↓
Notification Consumer

SQLite
↓
Flask + SocketIO Dashboard

---

## Kafka Topics

| Topic Name          | Purpose                     |
| ------------------- | --------------------------- |
| orders_v2           | Incoming customer orders    |
| delivery_updates_v2 | Delivery status updates     |
| retry_orders        | Failed orders for retry     |
| dead_letter_orders  | Permanently failed messages |
| notifications       | Delivery notifications      |

---

## Technologies Used

* Apache Kafka
* Python
* Flask
* Flask-SocketIO
* SQLite
* HTML
* CSS
* JavaScript
* Docker (In Progress)

---

## Project Structure

```text
order_producer.py
order_consumer.py
delivery_consumer.py
db_consumer.py
notification_service.py
notification_consumer.py
retry_consumer.py
dlq_consumer.py
app.py
food_delivery.db
templates/
screenshots/
```

## How to Run

### Start Kafka

```bash
zookeeper-server-start.bat config/zookeeper.properties

kafka-server-start.bat config/server.properties
```

### Start Services

```bash
python order_consumer.py

python delivery_consumer.py

python db_consumer.py

python notification_service.py

python notification_consumer.py

python retry_consumer.py

python app.py
```

### Generate Orders

```bash
python order_producer.py
```

### Open Dashboard

```text
http://127.0.0.1:5000
```

---

## Screenshots

### Dashboard

Add screenshots inside:

```text
screenshots/
```

Example:

```markdown
![Dashboard](screenshots/dashboard.png)
```

---

## Future Enhancements

* Docker Compose Deployment
* Kubernetes Deployment
* SMS/Email Notification Integration
* Machine Learning Based Demand Prediction
* Cloud Deployment (AWS)

---

## Author

Tanishq Vijay Bhoyar

Electronics and Communication Engineering

Apache Kafka | Python | Real-Time Systems | Distributed Systems
