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
				result = analyzeWords(sentence)

		#print sentences

def analyzeWords(sentence):

	tokens = nltk.Text(nltk.word_tokenize(sentence))
	key = tokens.findall(r"<you><were><.*>{3,}")

splitSentences()

