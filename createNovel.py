from sys import argv
import sqlite3
from random import randrange
import datetime

#create an optional argument for a city-specific novel
script, city = argv

#blank lists for types of sentences
intros = []
descriptions = []
interactions = []
more = []
afterthoughts = []

#initialize blank list, this is where we are storing the novel
novel = []

def selectSentence(type):

	seed = randrange(len(type))
	return seed

def printNovel():

	#generates a unique file name with the city and the date/time
	pubdate = datetime.datetime.now()
	filename = city + "-" + pubdate.strftime("%B%d%y-%I%M%p") + ".txt"

	#pick a first sentence at random from the list, append it to the novel lis
	firstSentence = selectSentence(intros)
	novel.append(intros[firstSentence])
	currentSentence = 0
	count = len(intros[firstSentence])

	#while the total character count is less than 5000...
	while count < 5000:

		#picking new sentence type based on last sentence type
		#intro sentence is only used at the beginning.  the other types cycle through.

		if currentSentence == 0:

			nextSentence = selectSentence(descriptions)
			currentSentence = 1
			novel.append(descriptions[nextSentence])

		if currentSentence == 1:
			nextSentence = selectSentence(interactions)
			currentSentence = 2
			novel.append(interactions[nextSentence])

		if currentSentence == 2:
			nextSentence = selectSentence(more)
			currentSentence = 3
			novel.append(more[nextSentence])

		if currentSentence == 3:
			nextSentence = selectSentence(afterthoughts)
			currentSentence = 4
			novel.append(afterthoughts[nextSentence])

		if currentSentence == 4:
			nextSentence = selectSentence(descriptions)
			currentSentence = 1
			novel.append(descriptions[nextSentence])

		#adding the length of the last sentence to the total character count, determines whether the loop runs again
		count += len(descriptions[nextSentence])

	#put a final afterthought sentence to end the novel
	nextSentence = selectSentence(afterthoughts)
	novel.append(afterthoughts[nextSentence])

	#writing to a text file
	file = open(filename, "w")

	#looping through novel list and writing each sentence to the file
	for sentence in novel:
		file.write(sentence + ". ")

	file.close()

	print count
	print "Novel is generated at " + filename



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

	category = result[3]
	sentence = result[2]

	if category == "intro":
		intros.append(sentence)
	elif category == "description":
		descriptions.append(sentence)
	elif category == "interaction":
		interactions.append(sentence)
	elif category == "afterthought":
		afterthoughts.append(sentence)
	elif category == "more":
		more.append(sentence)

#call printNovel to print result
printNovel()


