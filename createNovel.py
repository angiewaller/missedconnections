import re
import sqlite3
from random import randrange
import datetime
import os

#create optional arguments for a city-specific, directionally-specific (ie, w4m/m4w/w4w/m4m), or thematic novel
#set up optional city variable
city_input = raw_input("Please enter the city you want.  If none, hit return: ")

if city_input != "":
	city = city_input
else:
	city = "all"
print city

#set up optional orientation variable
direction_input = raw_input("Please enter an orientation you want.  If none, hit return: ")

if direction_input != "":
	direction = direction_input
else:
	direction = "all"
print direction

#setting up optional theme for novel
theme = []
theme_file = raw_input("Please enter the name of the theme file.  If none, hit return: ")
print len(theme)

#!!! CHANGE ORDER OF SENTENCE TYPES HERE !!!
content = ["intro", "description", "interaction", "more", "afterthought"]
content_lists = []

#blank lists for types of sentences

for c in content:
	c = []
	content_lists.append(c)

#initialize blank list, this is where we are storing the novel and the IDs of all the sentences in it
novel = []
ids = []

#setting up lists for the pronoun exchanges; change file here
fromWords = []
toWords = []
fromFile = "from.txt"
toFile = "w4m.txt"

def selectSentence(type):

	seed = randrange(len(type))
	return seed

def printNovel():

	#generates a unique file name with the city and the date/time
	pubdate = datetime.datetime.now()
	filename = "novels/" + city + "-" + pubdate.strftime("%B%d%y-%I%M%p") + ".txt"
	dir = os.path.dirname(filename)
	if not os.path.exists(dir):
		os.makedirs(dir)

	#pick a intros sentence at random from the list, append it to the novel list
	introsSentence = selectSentence(content[0])
	novel.append(content_lists[0][introsSentence][0])
	# print content_lists[0][introsSentence][0]
	ids.append(content_lists[0][introsSentence][1])

	currentSentence = 0
	count = len(content_lists[0][introsSentence][0])

	#while the total character count is less than 5000...
	while count < 1000:

		total = len(content)-1

		#picking new sentence type based on last sentence type
		#first type of sentence is only used at the beginning.  the other types cycle through.

		if currentSentence == total:
			nextSentence = selectSentence(content[total])
			newcopy = content_lists[total][nextSentence][0]
			newid = content_lists[total][nextSentence][1]

			novels_set = set(novel)

			if newcopy in novels_set:
				print "Found a " + content[i] + "match!  Trying again."
				currentSentence = i

			else:
				novel.append(newcopy)
				ids.append(newid)
				currentSentence = 1
				print newcopy

				#adding the length of the last sentence to the total character count, determines whether the loop runs again
				count += len(novel[-1])

		else:
			for i in range(0, total):
					if currentSentence == i:
						# print currentSentence
						nextSentence = selectSentence(content[i+1])
						newcopy = content_lists[i+1][nextSentence][0]
						newid = content_lists[i+1][nextSentence][1]

						novels_set = set(novel)

						if newcopy in novels_set:
							print "Found a " + content[i] + "match!  Trying again."
							currentSentence = i

						else:
							novel.append(newcopy)
							ids.append(newid)
							currentSentence = i+1
							print newcopy
							count += len(novel[-1])

	#put a final sentence to end the novel
	nextSentence = selectSentence(content_lists[len(content)-1])
	novel.append(content_lists[len(content)-1][nextSentence][0])

	#writing to a text file
	file = open(filename, "w")

	#looping through novel list, cleaning up the text a little, and writing each sentence to the file
	for sentence in novel:
		sentence = sentence.strip()
		sentence = sentence.lower()
		for i in range(0,len(fromWords)):
			sentence = sentence.replace(fromWords[i], toWords[i])
		sentence = sentence.capitalize()
		sentence = sentence.replace("i'd", "I'd").replace("i'm", "I'm").replace(" i ", " I ").replace("i'll", "I'll")

		#print sentence
		file.write(sentence + ". ")

	file.close()

	print "Novel is generated at " + filename + ", count of " + str(count) + " characters"


def loadFromFile(filename, destination):

	file = open("dictionaries/" + filename, "r")
	phrases = file.read()
	phrases = phrases.split('\n')

	for phrase in phrases:
		destination.append(phrase)

	#print destination


#load theme file
if theme_file != "":
	loadFromFile(theme_file, theme)
else:
	theme.append(' ')
# print len(theme)

#connect to the database
conn = sqlite3.connect('novelsDB.db')
c = conn.cursor()
conn.text_factory = str

if city == "all" and direction == "all":

	#select from all the db entries, doesn't matter what city or what direction
	c.execute('SELECT * from sentences')
	results = c.fetchall()

elif city == "all" and direction != "all":
	#select from all entries where the direction matches, regardless of city
	c.execute('SELECT * from sentences WHERE direction=:theDirection',
		{"theDirection": direction})
	results = c.fetchall()

elif city != "all" and direction == "all":
	#select from all entries where the direction matches, regardless of city
	c.execute('SELECT * from sentences WHERE city=:theCity',
		{"theCity": city})
	results = c.fetchall()

else:
	#select all db entries where the city matches the city argument AND the direction matches the direction argument
	c.execute('SELECT * from sentences WHERE city=:theCity AND direction=:theDirection',
		{"theCity":city, 'theDirection':direction})
	results = c.fetchall()

#adding cities to lists by category of sentence
for result in results:

	category = result[4]
	sentence = result[3]
	id = result[0]

	if len(theme) > 1:
		for word in theme:
			if word in sentence:

				for c in content:
					if category == c:
						i = content.index(c)
						content_lists[i].append([sentence, id])

	else:
		for c in content:
			if category == c:
				i = content.index(c)
				content_lists[i].append([sentence, id])
		

#create pronoun exchange lists
loadFromFile(fromFile, fromWords)
loadFromFile(toFile, toWords)

#call printNovel to print result
printNovel()


