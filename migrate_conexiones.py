import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

host = os.getenv("MYSQL_HOST", "149.34.48.176")
user = os.getenv("MYSQL_USER", "admin")
password = os.getenv("MYSQL_PASSWORD", "marymar123")
database = os.getenv("MYSQL_DB", "datagenerator_db")
port = int(os.getenv("MYSQL_PORT", 3307))

conn = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
cur = conn.cursor()

queries = [
    "ALTER TABLE conexiones ADD COLUMN IF NOT EXISTS nombre_alias VARCHAR(100) NULL",
    "ALTER TABLE conexiones ADD COLUMN IF NOT EXISTS usuario_db VARCHAR(255) NULL",
    "ALTER TABLE conexiones ADD COLUMN IF NOT EXISTS password_db TEXT NULL",
]

for sql in queries:
    try:
        cur.execute(sql)
        print(f"OK: {sql[:70]}")
    except Exception as e:
        print(f"Skip ({e})")

conn.commit()
conn.close()
print("DONE")
