import nltk
import sqlite3
import re

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
		copy = item[5]

		#replacing unusable characters and splitting the copy into sentences
		copy = copy.strip()
		copy = copy.replace('\n', '').replace('[...]', '').replace("'", "\'")
		sentences = copy.split('.')

		for sentence in sentences:
			if sentence == '':
				sentences.remove(sentence)

			#if there is actually something there, run the sortPhrases function to add tags for the type of sentence this is
			if len(sentence) > 0:
				results = sortPhrases(sentence)

				if len(results) > 0:
					for result in results:
						#add new sentences to a database for the type of sentence, keeping city and category attached
						addEntry(id, sentence, city, result)

	conn.close()

	db = sqlite3.connect('novelsDB.db')
	cur = db.cursor()
	db.text_factory = str
	cur.execute('SELECT * FROM sentences ORDER BY id DESC LIMIT 1')
	lastEntry = cur.fetchall()[0]

	print "Analysis complete.  Last sentence analyzed: " + str(lastEntry[0]) + ", " + lastEntry[2]


def sortPhrases(sentence):

	tags = []

	#eventually turn these into YAML dictionaries or the like
	intro = ["You were", "I was", "I pulled up", "I swear", "I know", "I saw", "You saw"]
	interaction = ["nodded", "shared", "called", "talk", "talking", "we met", "locked eyes", "stared", "looked", "looking for", "smiled"]
	description = ["looked like", "saw", "were reading", "was reading", "ogle", "ogled", "ogling", "got in"]
	more = ["commented", "you bought", "turned", "was there", "shared", "exchanged", "told you", "told me", "you're not", "got there", "thinking"]
	afterthought = ["I believe", "I feel", "felt like", "think about", "I think", "I thought", "forgot", "wanted", "didn't want"]

	#for all the categories: if there's a match found, add a tag to the sentence
	for phrase in intro:
		key = re.match(phrase, sentence)
		if key != None:
			tags.append("intro")
			break

	for phrase in interaction:
		key = re.search(phrase, sentence)
		if key != None:
			tags.append("interaction")
			break

	for phrase in description:
		key = re.search(phrase, sentence)
		if key != None:
			tags.append("description")
			break

	for phrase in afterthought:
		key = re.search(phrase, sentence)
		if key != None:
			tags.append("afterthought")
			break

	for phrase in more:
		key = re.search(phrase, sentence)
		if key != None:
			tags.append("more")
			break

	return tags


#adding entries to the database
def addEntry(id, sentence, city, category):

	db = sqlite3.connect('novelsDB.db')
	cur = db.cursor()
	db.text_factory(str)

	cur.execute('SELECT max(id) FROM sentences')
	result = cur.fetchone()
	lastID = result[0]
	# print lastID

	if id > lastID:

		toAdd = (id, city, sentence, category)
		cur.execute('INSERT INTO sentences VALUES (?, ?, ?, ?)', toAdd)

		db.commit()

	db.close()



splitSentences()

