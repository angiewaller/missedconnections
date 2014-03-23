import sqlite3

conn = sqlite3.connect('novelsDB.db')

c = conn.cursor()

c.execute('''CREATE TABLE sentences
             (city text, copy text, category text)''')

conn.commit()
conn.close()