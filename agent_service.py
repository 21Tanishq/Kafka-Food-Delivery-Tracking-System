import sqlite3
import time
import random

conn = sqlite3.connect("food_delivery.db", check_same_thread=False)
cursor = conn.cursor()

print("Agent Service Started")

while True:

    cursor.execute("""
        SELECT order_id
        FROM order_events
        WHERE status='OUT_FOR_DELIVERY'
    """)

    orders = cursor.fetchall()

    for order in orders:

        order_id = order[0]

        cursor.execute("""
            SELECT agent_id
            FROM agents
            WHERE current_order=?
        """, (order_id,))

        if cursor.fetchone():
            continue

        cursor.execute("""
            SELECT agent_id
            FROM agents
            WHERE status='AVAILABLE'
            LIMIT 1
        """)

        agent = cursor.fetchone()

        if agent:

            agent_id = agent[0]

            cursor.execute("""
                UPDATE agents
                SET status='BUSY',
                    current_order=?
                WHERE agent_id=?
            """, (order_id, agent_id))

            print(
                f"Assigned Order {order_id} "
                f"to Agent {agent_id}"
            )

            conn.commit()

    time.sleep(5)
cursor.execute("""
    SELECT order_id
    FROM order_events
    WHERE status='DELIVERED'
""")

delivered_orders = cursor.fetchall()

for order in delivered_orders:

    order_id = order[0]

    cursor.execute("""
        UPDATE agents
        SET status='AVAILABLE',
            current_order=NULL
        WHERE current_order=?
    """, (order_id,))

conn.commit()