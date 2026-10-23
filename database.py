#database file
#will need to be run before running main when it is implemented
#status: not yet integrated
#no need to run this file yet

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
cursor.execute("""CREATE TABLE IF NOT EXISTS soup_storage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    soup TEXT NOT NULL,
                    url TEXT NOT NULL)""")

conn.commit()

#basically testing from here
url1 = "https://www.scrapethissite.com/lessons/"
url2 = "https://www.scrapethissite.com/pages/"

response1 = requests.get(url1, timeout = 20)
response2 = requests.get(url2, timeout = 20)

soup1 = 0
soup2 = 0

if response1.status_code == 200:
    soup1 = BeautifulSoup(response1.text, "html.parser")

if response2.status_code == 200:
    soup2 = BeautifulSoup(response2.text, "html.parser")

cursor.execute("""INSERT OR REPLACE INTO soup_storage (soup, url) VALUES (?, ?)""",(str(soup1), url1))

conn.commit()

cursor.execute("SELECT * FROM soup_storage")

print(cursor.fetchall())

#to retrieve soup back from the db
# cursor.execute("SELECT soup FROM soup_storage WHERE url = ?", (url1,))
# result = cursor.fetchone()
#
# soup_html = result[0]
# soup1 = BeautifulSoup(soup_html, "html.parser")

conn.close()

