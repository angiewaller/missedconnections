import sqlite3

conn = sqlite3.connect('sampleDB.db')
myCities=["newyork","chicago","losangeles","delaware"]
myCategories = ["w4m","m4m", "m4w", "w4w"]

#myCities=["newyork"]
#myCategories = ["m4m"]
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE listings
             (id int, city text, date text, category text, title text, copy text, link text)''')

c.execute('''CREATE TABLE lastID
             (id int, value int)''')

toAdd =(0,0)
c.execute('INSERT INTO lastID VALUES (?,?)', toAdd)
conn.commit()

c.execute('''CREATE TABLE lastURLS
            (city text, feed text, url text, category text, title text)''')




for city in myCities:
        for category in myCategories:
            theFeed = 'http://' + city + '.craigslist.org/search/mis/?query='+ category +'&format=rss'
            toAdd = (city, theFeed, "nothing", category, "blank")
            c.execute('INSERT INTO lastURLS VALUES (?,?,?,?,?)', toAdd)
            conn.commit()
            print theFeed + " added!"

conn.close()


