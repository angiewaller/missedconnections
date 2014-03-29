import feedparser
import sqlite3
import threading

#this function loads all the URLs for different cities and categories we'll use. 
def loadCityAndCat():
	#get a feed url and listing 
	conn = sqlite3.connect('sampleDB.db')
	c = conn.cursor()
	conn.text_factory = str
	c.execute('SELECT * FROM lastURLS')
	result = c.fetchall()
	for item in result:

		print "getting feeds from " + item[0] + " in category " + item[3]		
		#collect info from feeds
		getLastURL(item[1], item[2], item[0], item[3], item[4])

	#call getText again to keep the program going
	getText()


def getLastURL(theFeed, theURL, theCity, theCategory, theTitle):
	
	d = feedparser.parse(theFeed)	
	#make sure the call was successful
	if (d.feed.has_key('title')):
		d['feed']['title']
		
		#if there's no URL in the db yet:
		if theURL == "nothing":
			getFirstListings(d, theCity, theCategory, theFeed)
			
		else:
			updateListings(theCity, theFeed, theURL, theCategory, theTitle)
			newInfo = updateLastURL(d, theFeed)
			newUrl = newInfo[0]
			newTitle = newInfo[1]
			print "most recent entry: " + newTitle

				
#fills in the db with initial info		
def getFirstListings(feed, theCity, theCategory, theFeed):

	conn = sqlite3.connect('sampleDB.db')
	c = conn.cursor()
	conn.text_factory = str
	#we need to add the unique ID for each new listing. get the lastID and updated it by 1 
	c.execute('SELECT value FROM lastID WHERE id=0')
	row = c.fetchone()
	saveID = row[0]

	if len(feed.entries) > 0:
		for listing in feed.entries:
			saveTitle = listing.title
			saveDate = listing.date
			saveDescription = listing.description
			saveLink = listing.link
			#increment saveID
			saveID+=1
			#make an array for the db input
			toSave=(saveID,theCity, saveDate, theCategory, saveTitle, saveDescription, saveLink)
			#connect and insert the row to the database
			c.execute('INSERT INTO listings VALUES (?,?,?,?,?,?,?)', toSave)
			conn.commit()

		#insert the last ID into database
		c.execute("UPDATE lastID SET value=? WHERE id=?", (saveID, 0))
		conn.commit()

		firstLink = feed.entries[0].link
		firstTitle = feed.entries[0].title.replace('"', '').replace("'", "")

		c.execute('UPDATE lastURLS SET url="'+firstLink+'" WHERE feed="'+theFeed+'"')
		c.execute('UPDATE lastURLS SET title="'+firstTitle+'" WHERE feed="'+theFeed+'"')
		conn.commit()
		conn.close()

		print "SAVED FIRST PASS"
		print firstTitle

	else:

		print "RSS feed empty :("


    
#updates the latest URL to check against
def updateLastURL(feed, theFeed):

	newInfo = []
	
	conn = sqlite3.connect('sampleDB.db')
	c = conn.cursor()
	conn.text_factory = str

	if len(feed.entries) > 0:
				
		#add value of the first element in the feed to the lastURLS database
		latestURL = feed.entries[0].link
		latestTitle = feed.entries[0].title.replace('"', '').replace("'", "")

	else:

		latestURL = "nothing"
		latestTitle = ""
	
	newInfo.append(latestURL)
	newInfo.append(latestTitle)
		
	c.execute('UPDATE lastURLS SET url="'+latestURL+'" WHERE feed="'+theFeed+'"')
	c.execute('UPDATE lastURLS SET title="'+latestTitle+'" WHERE feed="'+theFeed+'"')
    
	conn.commit()
	conn.close()
	
	return newInfo


#updates all the listings	
def updateListings(theCity, theFeed, lastURL, theCategory, theTitle):
	d = feedparser.parse(theFeed)
	#make sure the call was successful
	if (d.feed.has_key('title')):
		d['feed']['title']

		for listing in d.entries:
			conn = sqlite3.connect('sampleDB.db')
			c = conn.cursor()
			conn.text_factory = str
			
			#get last ID value
			c.execute('SELECT value FROM lastID WHERE id=0')
			row = c.fetchone()
			lastID = row[0]
			newID = lastID
			
			if listing.link != lastURL and listing.title != theTitle:
				#we have a new listing!
				newID += 1
				newTitle = listing.title.replace('"', '').replace("'", "")
				newDate = listing.date
				newLink = listing.link
				newDescription = listing.description
				
				toSave = (newID, theCity, newDate, theCategory, newTitle, newDescription, newLink)
				
				c.execute('INSERT INTO listings VALUES (?,?,?,?,?,?,?)', toSave)
				conn.commit()
				
				c.execute("UPDATE lastID SET value=? WHERE id=?", (newID, 0))
				conn.commit()
				conn.close()
				
				print "****NEW LISTING: " + newTitle + ", " + newLink + "****"
			
			else:
				#this listing is already in our db and we can stop looking
				print "NO NEW FRIENDS for " + theCategory + " in " + theCity
				break
   

def getText():
    print "give these people some time to connect..."
    t = threading.Timer(50.0,loadCityAndCat)
    t.start()

getText()

