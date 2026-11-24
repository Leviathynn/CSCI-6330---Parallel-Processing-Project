#database file
#will need to be run before running main
#can be run again to reset the database

import sqlite3
import requests
from bs4 import BeautifulSoup

#db name
db = "soup_storage.db"

#starts and connects to the db or
#creates it if it doesn't exist
conn = sqlite3.connect(db)
cursor = conn.cursor()

#makes a table if it doesn't exist. The format is
#id = autoincrement, soup = text, url = text
cursor.execute("DROP TABLE IF EXISTS soup_storage")

cursor.execute("""CREATE TABLE IF NOT EXISTS soup_storage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_words TEXT NOT NULL,
                    url TEXT NOT NULL)""")

conn.commit()



#testing to print out the empty table to indicate the table
#was successfully made

#grabs column names
cursor.execute("PRAGMA table_info(soup_storage)")

columns = cursor.fetchall()
col_list = []

for col in columns:
    col_list.append(col[1])

print(col_list)

#grabs all rows
cursor.execute("SELECT * FROM soup_storage")

print(cursor.fetchall())

print("Database Remade Successfully")

conn.close()
