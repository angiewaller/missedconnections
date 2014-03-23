from sys import argv
import sqlite3
from random import randrange

script, city = argv

intros = []
descriptions = []
interactions = []
afterthoughts = []

def printNovel():

	introSelect = randrange(len(intros))
	descSelect = randrange(len(descriptions))
	interSelect = randrange(len(interactions))
	afterSelect = randrange(len(afterthoughts))
	print intros[introSelect] + ".  " + descriptions[descSelect] + ".  " + interactions[interSelect] + ".  " + afterthoughts[afterSelect] + "."

conn = sqlite3.connect('novelsDB.db')
c = conn.cursor()
conn.text_factory(str)

# if len(sys.argv) > 1:

c.execute('SELECT * from sentences where city=:theCity', 
	{"theCity": city})
results = c.fetchall()

for result in results:

	category = result[2]
	sentence = result[1]

	if category == "intro":
		intros.append(sentence)
	elif category == "description":
		descriptions.append(sentence)
	elif category == "interaction":
		interactions.append(sentence)
	elif category == "afterthought":
		afterthoughts.append(sentence)

printNovel()

#print result
