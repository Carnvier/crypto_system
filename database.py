import sqlite3
import pandas as pd

conn = sqlite3.connect('crypto.db')

cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS crypto_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        price REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
)


df = pd.read_sql("SELECT * FROM crypto_prices", conn)
df.head()

conn.commit()
cursor.close()
conn.close()

print("Database created successfully.")