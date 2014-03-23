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
		copy = copy.strip()
		copy = copy.replace('\n', '').replace('[...]', '').replace("'", "\'")
		sentences = copy.split('.')

		for sentence in sentences:
			if sentence == '':
				sentences.remove(sentence)

			if len(sentence) > 0:
				result = sortPhrases(sentence)

				if len(result) > 0:
					print result

					# if result[0] == "intro":
					# 	print sentence

		#print sentences

def sortPhrases(sentence):

	tags = []

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


splitSentences()

