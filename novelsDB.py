#run this once to create a database for the sentences to be used in the novels

import sqlite3

conn = sqlite3.connect('novelsDB.db')

c = conn.cursor()

c.execute('''CREATE TABLE sentences
             (id int, direction text, city text, copy text, category text)''')

conn.commit()
conn.close()