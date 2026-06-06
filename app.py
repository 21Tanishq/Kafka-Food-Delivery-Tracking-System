from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


# ==========================
# GET LATEST ORDER STATUS
# ==========================
def get_latest_data():

    conn = sqlite3.connect("food_delivery.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o1.order_id, o1.status, o1.timestamp
        FROM order_events o1
        WHERE o1.id = (
            SELECT MAX(o2.id)
            FROM order_events o2
            WHERE o2.order_id = o1.order_id
        )
        ORDER BY o1.order_id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================
# HOME PAGE
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# SOCKET CONNECT
# ==========================
@socketio.on("connect")
def handle_connect():
    socketio.emit("update", get_latest_data())


# ==========================
# ACTIVITY FEED
# ==========================
@app.route("/events")
def get_events():

    conn = sqlite3.connect("food_delivery.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT order_id, status, timestamp
        FROM order_events
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)


# ==========================
# ANALYTICS
# ==========================
@app.route("/analytics")
def analytics():

    conn = sqlite3.connect("food_delivery.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM orders
    """)
    revenue = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(AVG(amount),0)
        FROM orders
    """)
    avg_order = round(cursor.fetchone()[0], 2)

    cursor.execute("""
        SELECT food, COUNT(*)
        FROM orders
        GROUP BY food
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    top_food = result[0] if result else "N/A"

    conn.close()

    return jsonify({
        "total_orders": total_orders,
        "revenue": revenue,
        "avg_order": avg_order,
        "top_food": top_food
    })


# ==========================
# REVENUE CHART DATA
# ==========================
@app.route("/revenue_history")
def revenue_history():

    conn = sqlite3.connect("food_delivery.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT order_id, amount
        FROM orders
        ORDER BY order_id
    """)

    rows = cursor.fetchall()

    conn.close()

    labels = []
    values = []

    running_revenue = 0

    for order_id, amount in rows:

        running_revenue += amount

        labels.append(f"Order {order_id}")
        values.append(running_revenue)

    return jsonify({
        "labels": labels,
        "values": values
    })
@app.route("/agents")
def agents():

    conn = sqlite3.connect("food_delivery.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name,status,current_order
        FROM agents
    """)

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)
@app.route("/agent_stats")
def agent_stats():

    conn = sqlite3.connect("food_delivery.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM agents
        WHERE status='BUSY'
    """)

    busy = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM agents
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "busy": busy,
        "total": total
    })
@app.route("/notifications")
def get_notifications():

    conn = sqlite3.connect("food_delivery.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            message TEXT,
            type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        SELECT order_id, message, type, timestamp
        FROM notifications
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)
@app.route("/system_stats")
def system_stats():
    conn = sqlite3.connect("food_delivery.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM notifications")
    notifications = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    orders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM order_events")
    events = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "notifications": notifications,
        "orders": orders,
        "events": events
    })

# ==========================
# START SERVER
# ==========================
if __name__ == "__main__":
    socketio.run(app, debug=True)