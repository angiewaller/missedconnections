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


Project for [Angie Waller](http://angiewaller.com/)
Scraping code completed with [Zannah Marsh](http://zannahbot.com/).