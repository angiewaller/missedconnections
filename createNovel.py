from sys import argv
import re
import sqlite3
from random import randrange
import datetime
import os

#create optional argument for a city-specific and directionally-specific (ie, w4m/m4w/w4w/m4m) novel
if len(argv) > 2:
	script, direction, city = argv
elif len(argv) > 1:
	script, direction = argv
	city = "all"
else:
	direction = "all"
	city = "all"


#blank lists for types of sentences
intros = []
descriptions = []
interactions = []
more = []
afterthoughts = []

#initialize blank list, this is where we are storing the novel and the IDs of all the sentences in it
novel = []
ids = []

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

	#pick a first sentence at random from the list, append it to the novel list
	firstSentence = selectSentence(intros)
	novel.append(intros[firstSentence][0])
	print intros[firstSentence][0]
	ids.append(intros[firstSentence][1])
	currentSentence = 0
	count = len(intros[firstSentence][0])

	#while the total character count is less than 5000...
	while count < 5000:

		#picking new sentence type based on last sentence type
		#intro sentence is only used at the beginning.  the other types cycle through.

		if currentSentence == 0:

			nextSentence = selectSentence(descriptions)
			newcopy = descriptions[nextSentence][0]
			newid = descriptions[nextSentence][1]

			#create a set out of all the ids & novels in the lists so far
			id_set = set(ids)
			novels_set = set(novel)

			#checking for duplicates, first against the id
			if newid in id_set:
				print "Found a duplicate.  Checking..."

				#if an id dupe found, check against the sentences in the novel.  if found, keep currentSentence the same and try again
				if newcopy in novels_set:
					print "Found a description match! Trying again."
					currentSentence = 0	

				#if sentence is not the same, OK to add to novel		
				else:
					novel.append(newcopy)
					ids.append(newid)
					currentSentence = 1

			#if id is not the same, OK to add to novel
			else:
				novel.append(newcopy)
				ids.append(newid)
				currentSentence = 1
			# print currentSentence

		#repeat above for the rest of the sentence types
		#interactions
		if currentSentence == 1:

			nextSentence = selectSentence(interactions)
			newcopy = interactions[nextSentence][0]
			newid = interactions[nextSentence][1]
			id_set = set(ids)
			novels_set = set(novel)

			if newid in id_set:
				print "Found a duplicate.  Checking..."
				if newcopy in novels_set:
					print "Found an interaction match! Trying again."
					currentSentence = 1			
				else:
					novel.append(newcopy)
					ids.append(newid)
					currentSentence = 2

			else:
				novel.append(newcopy)
				ids.append(newid)
				currentSentence = 2
			# print currentSentence

		#more action
		if currentSentence == 2:
			nextSentence = selectSentence(more)
			newcopy = more[nextSentence][0]
			newid = more[nextSentence][1]
			id_set = set(ids)
			novels_set = set(novel)

			if newid in id_set:
				print "Found a duplicate.  Checking..."
				if newcopy in novels_set:
					print "Found a 'more action' match! Trying again."
					currentSentence = 2			
				else:
					novel.append(newcopy)
					ids.append(newid)
					currentSentence = 3

			else:
				novel.append(newcopy)
				ids.append(newid)
				currentSentence = 3
			# print currentSentence

		#afterthoughts
		if currentSentence == 3:
			nextSentence = selectSentence(afterthoughts)
			newcopy = afterthoughts[nextSentence][0]
			newid = afterthoughts[nextSentence][1]
			id_set = set(ids)
			novels_set = set(novel)

			if newid in id_set:
				print "Found a duplicate.  Checking..."
				if newcopy in novels_set:
					print "Found an afterthoughts match! Trying again."
					currentSentence = 3		
				else:
					novel.append(newcopy)
					ids.append(newid)
					currentSentence = 1

			else:
				novel.append(newcopy)
				ids.append(newid)
				currentSentence = 1
			# print currentSentence

		#adding the length of the last sentence to the total character count, determines whether the loop runs again
		count += len(novel[-1])

	#put a final afterthought sentence to end the novel
	nextSentence = selectSentence(afterthoughts)
	novel.append(afterthoughts[nextSentence][0])

	#writing to a text file
	file = open(filename, "w")

	#looping through novel list, cleaning up the text a little, and writing each sentence to the file
	for sentence in novel:
		sentence = sentence.strip()
		sentence = sentence.lower()
		for i in range(0,len(fromWords)):
			sentence = sentence.replace(fromWords[i], toWords[i])
		sentence = sentence.capitalize()
		sentence = sentence.replace("i'd", "I'd").replace("i'm", "I'm").replace(" i ", " I ")

		# print sentence
		file.write(sentence + ". ")

	file.close()

	print "Novel is generated at " + filename + ", count of " + str(count) + " characters"
	# print ids

def loadFromFile(filename, destination):

	file = open("dictionaries/" + filename, "r")
	phrases = file.read()
	phrases = phrases.split('\n')

	for phrase in phrases:
		destination.append(phrase)

	# print destination


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

	if category == "intro":
		intros.append([sentence, id])
	elif category == "description":
		descriptions.append([sentence, id])
	elif category == "interaction":
		interactions.append([sentence, id])
	elif category == "afterthought":
		afterthoughts.append([sentence, id])
	elif category == "more":
		more.append([sentence, id])

loadFromFile(fromFile, fromWords)
loadFromFile(toFile, toWords)

#call printNovel to print result
printNovel()


