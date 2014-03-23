from sys import argv
import sqlite3
from random import randrange

#create an optional argument for a city-specific novel
script, city = argv

#blank lists for types of sentences
intros = []
descriptions = []
interactions = []
afterthoughts = []

def printNovel():

	#pick a sentence at random from the list and print it
	introSelect = randrange(len(intros))
	descSelect = randrange(len(descriptions))
	interSelect = randrange(len(interactions))
	afterSelect = randrange(len(afterthoughts))
	print intros[introSelect] + ".  " + descriptions[descSelect] + ".  " + interactions[interSelect] + ".  " + afterthoughts[afterSelect] + "."


#connect to the database
conn = sqlite3.connect('novelsDB.db')
c = conn.cursor()
conn.text_factory(str)

# if len(sys.argv) > 1:

#select all db entries where the city matches the city argument
c.execute('SELECT * from sentences where city=:theCity', 
	{"theCity": city})
results = c.fetchall()

#adding cities to lists by category of sentence
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

#call printNovel to print result
printNovel()


