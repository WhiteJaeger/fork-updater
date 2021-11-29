import sqlite3
import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

connection = sqlite3.connect('database.db')


with open(os.path.join(CUR_DIR, 'schema.sql')) as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO forks (name, url, status) VALUES (?, ?, ?)",
            ('test', 'test-url', 'test-status')
            )

connection.commit()
connection.close()
