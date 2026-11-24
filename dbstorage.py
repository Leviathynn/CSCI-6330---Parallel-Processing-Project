#db related functions. sqlite3 database needs to be made
#by running database.py once. database.py will restart the
#database by removing and remaking. Functions include
#store_url_info(url) and db_print().

import sqlite3
import requests
from bs4 import BeautifulSoup
from collections import Counter
import pandas as pd

#store_url_info takes in one url, gets the most common set of words
#(the amount of words gotten can be changed in variable "words_to_store")
#and stores the url and words in the database. The words will exclude
#filter words like "the", "and", "a" etc. These can be expanded up by
#adding them to the "filter_words" list.
#This function can be changed to store anything in the storage section
#Current db setup is {id, key_words, url} with key_words interchangeable
#with any text that wants to be stored.
def store_url_info(url):

    #amount of words to store in the database and the filter list
    #of words. This should match the "filter_list" in "soupTesting.py"
    #but doesn't have to based on usage.
    words_to_store = 5
    filter_words = ["the", "a", "to", "and", "or", "and", "but",
                    "in", "that", "this", "of", "with", "for",
                    "was", "were", "am", "is", "are", "it", "from",
                    "has", "|"]

    #connection to the database
    db = "soup_storage.db"
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    #checks the given url is valid
    response1 = requests.get(url, timeout=20)
    soup1 = 0
    if response1.status_code == 200:
        soup1 = BeautifulSoup(response1.text, "html.parser")


    soup1_contents = soup1.get_text().split()
    soup1_contents_filtered = []

    #filters the text and removes all characters irrelevant
    #for determining the topic of the page. Values can be added
    #here by adding ".replace(<removed_char>,"") to the list
    for text in soup1_contents:
        if text.lower() not in filter_words:
            soup1_contents_filtered.append(text.replace(".", "")
                                           .replace("(", "").replace(")", "")
                                           .replace("[", "").replace("]", "")
                                           .replace("{", "").replace("}", "")
                                           .replace(",", "").replace(":", "")
                                           .replace(";", "").replace("?", ""))

    #same as the section in "soupTesting.py"
    #counts all the times a word appears and gets the most common
    #amount of the amount determined earlier and makes it set
    soup1_count = Counter(soup1_contents_filtered)
    soup1_most_common = soup1_count.most_common(words_to_store)
    soup1_common_set = set()
    for text, count in soup1_most_common:
        soup1_common_set.add(text)

    #adds the set of common words and url to the database
    cursor.execute("""INSERT OR REPLACE INTO soup_storage (key_words, url) VALUES (?,? )""",
                   (str(soup1_common_set), url))
    conn.commit()

    conn.close()
    #print(soup1_common_set)



#prints the contents of the database in a formatted table
#format uses pandas.
def db_print():

    conn = sqlite3.connect("soup_storage.db")

    df = pd.read_sql_query("SELECT * FROM soup_storage", conn)
    print(df.to_string(index=False))

    conn.close()


#non-pandas print function. historical and testing use
def nonPdsPrint():

    conn = sqlite3.connect("soup_storage.db")
    cursor = conn.cursor()

    #gets the column names and prints them
    cursor.execute("PRAGMA table_info(soup_storage)")
    columns = cursor.fetchall()
    col_list = []
    for col in columns:
        col_list.append(col[1])
    print(col_list)

    #gets all contents from the database and print them
    cursor.execute("SELECT * FROM soup_storage")
    all_rows = cursor.fetchall()
    for row in all_rows:
        print(row)

#test runs
#store_url_info("https://www.scrapethissite.com/pages/simple/")
#nonPdsPrint()
#db_print()