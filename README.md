# Missed Connections Novel Project

### Before using:

Make sure you have the following Python libraries installed:

* feedparser
* threading
* sqlite3

Threading and Sqlite3 should come with Python 2.7.6.  Instructions for installing Feedparser are [here](https://pypi.python.org/pypi/feedparser), or install via Pip on the command line.


### To scrape the data:

Navigate to the folder and run the following first in Terminal:

    python db.py

This will initialize the database with all 4 categories in however many cities you choose (you can add them to the "db.py" code).  Cities must be spelled the way they are in the Craigslist feed -- all one word, no capital letters, etc.

Once your database is set up, run the following:

	python collectListings.py

Keep this running for however long you want.  It will scrape all new listings from the RSS feed every 50 seconds until it is stopped.

To stop the code, press Ctrl+c in the terminal window and the code will terminate after it has finished its current scrape.


### To analyze collected text:  

Create a new database of sorted sentences by running the following ONCE:

	python novelsDB.py

Then, run the following as often as you wish:

	python analyzeText.py

This will analyze the newest entries in your database.  Run this whenever you have a new chunk of data you want to add to the sentences you pull from for the novel.  


### To create a novel:

Run the following:

	python createNovel.py

The script will prompt you for a city, an orientation (w4m/m4m/m4w/w4w), and a file name for thematic words.  Please enter these in EXACTLY how they appear on Craigslist or on your computer.  These entries will limit the sentences chosen from for the novel.  If you don't want to specify anything, just hit return at the prompt.

The novel will print to a file in a "novels" directory.  The file name will print to terminal when the novel is completed.  

Code written for a project by [Angie Waller](http://angiewaller.com/).  
Scraping code completed with [Zannah Marsh](http://zannahbot.com/).