import os
import sqlite3

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

connection = sqlite3.connect('database.db')

with open(os.path.join(CUR_DIR, 'schema.sql')) as f:
    connection.executescript(f.read())
