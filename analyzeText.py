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

		copy = item[5]
		city = item[1]
		copy = copy.strip()
		copy = copy.replace('\n', '').replace('[...]', '').replace("'", "\'")
		sentences = copy.split('.')

		for sentence in sentences:
			if sentence == '':
				sentences.remove(sentence)

			if len(sentence) > 0:
				results = sortPhrases(sentence)

				if len(results) > 0:
					for result in results:
						#add new sentences to a database for the type of sentence, keeping city and category attached
						addEntry(sentence, city, result)
						print result + ": " + sentence + ", " + city


def sortPhrases(sentence):

	tags = []

	#eventually turn these into YAML dictionaries or the like
	intro = ["You were", "I was", "I pulled up", "I swear", "I know", "I saw", "You saw"]
	interaction = ["nodded", "shared", "called", "talk", "talking", "we met", "locked eyes", "stared", "looked", "looking for", "smiled"]
	description = ["looked like", "saw", "were reading", "was reading", "ogle", "ogled", "ogling", "got in"]
	afterthought = ["I believe", "I feel", "felt like", "think about", "I think", "I thought", "forgot", "wanted", "didn't want"]

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

	return tags


def addEntry(sentence, city, category):

	db = sqlite3.connect('novelsDB.db')
	cur = db.cursor()
	db.text_factory(str)

	toAdd = (city, sentence, category)
	cur.execute('INSERT INTO sentences VALUES (?, ?, ?)', toAdd)

	db.commit()
	db.close()



splitSentences()

