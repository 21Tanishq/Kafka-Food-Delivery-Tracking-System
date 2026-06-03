import sqlite3

conn = sqlite3.connect("food_delivery.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS agents (
    agent_id INTEGER PRIMARY KEY,
    name TEXT,
    status TEXT,
    current_order INTEGER
)
""")

agents = [
    (1, "Agent-1", "AVAILABLE", None),
    (2, "Agent-2", "AVAILABLE", None),
    (3, "Agent-3", "AVAILABLE", None)
]

cursor.executemany("""
INSERT OR IGNORE INTO agents
(agent_id,name,status,current_order)
VALUES (?,?,?,?)
""", agents)

conn.commit()
conn.close()

print("Agents created")