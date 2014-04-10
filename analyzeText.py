import nltk
import sqlite3
import re

categories = ["stop", "intro", "description", "interaction", "more", "afterthought"]

def splitSentences():

	conn = sqlite3.connect('sampleDB.db')
	c = conn.cursor()
	conn.text_factory = str
	c.execute('SELECT * FROM listings')
	result = c.fetchall()

	for item in result:

		#pulling info about the post from the database
		id = item[0]
		city = item[1]
		direction = item[3]
		copy = item[5]

		#replacing unusable characters and splitting the copy into sentences
		copy = copy.strip()
		copy = copy.replace('\n', '').replace(' [...]', '').replace("'", "\'").replace('/', '').replace('<3', '').replace(':)', '').replace('!', '.').replace(';', '.').replace(',', '.').replace('-', '.')
		sentences = copy.split('.')

		for sentence in sentences:
			if sentence == '':
				sentences.remove(sentence)

			#if there is actually something there, run the sortPhrases function to add tags for the type of sentence this is
			if len(sentence) > 0:
				results = sortPhrases(sentence)

				if len(results) > 0:
					for sentType in results:
						#add new sentences to a database for the type of sentence, keeping city and category attached
						addEntry(id, direction, sentence, city, sentType)

	conn.close()

	db = sqlite3.connect('novelsDB.db')
	cur = db.cursor()
	db.text_factory = str
	cur.execute('SELECT * FROM sentences ORDER BY id DESC LIMIT 1')
	lastEntry = cur.fetchall()[0]

	print "Analysis complete.  Last sentence analyzed: " + str(lastEntry[0]) + ", " + lastEntry[2]


def sortPhrases(sentence):

	tags = []

	for category in categories:
		filename = category + ".txt"
		file = open('dictionaries/' + filename, 'r')
		phrases = file.read()
		phrases = phrases.split('\n')

		#tagging all the stuff that belongs in the stop list
		if category == "stop":
			for phrase in phrases:
				key = re.search(phrase, sentence)
				if key != None:
					tags.append(category)

		else:

			tag_set = set(tags)

			#sorting fragments by tags, filtering the ones that have already been tagged with "stop"
			for phrase in phrases:
				if category == "intro":

					key = re.match(phrase, sentence)
					if key != None and "stop" not in tag_set:
						tags.append(category)
						break

				else:

					key = re.search(phrase, sentence)
					if key != None and "stop" not in tag_set:
						tags.append(category)
						break

		file.close()

	return tags


#adding entries to the database
def addEntry(id, direction, sentence, city, category):

	db = sqlite3.connect('novelsDB.db')
	cur = db.cursor()
	db.text_factory = str

	cur.execute('SELECT max(id) FROM sentences')
	result = cur.fetchone()
	lastID = result[0]
	# print lastID

	if id > lastID and category != "stop":

		toAdd = (id, direction, city, sentence, category)
		cur.execute('INSERT INTO sentences VALUES (?, ?, ?, ?, ?)', toAdd)

		db.commit()

	db.close()



splitSentences()

