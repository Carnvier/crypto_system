import sqlite3

conn = sqlite3.connect('broker.db')

cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS brokers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        email TEXT NOT NULL,
        website TEXT NOT NULL
    )
    """
)

conn.commit()
cursor.close()
conn.close()

print("Broker database created successfully.")