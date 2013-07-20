#!/bin/python
# Sheldon Quotes

# Third Party Modules
from BeautifulSoup import BeautifulSoup
import sqlite3 as lite

# Standard Modules
import urllib2
import urllib # for urlencode
from urlparse import urljoin

URL = "http://the-big-bang-theory.com/quotes/character/Sheldon/%d/"
DB_NAME = "SheldonQuotes.db"

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def db_connect():
    con = lite.connect(DB_NAME)
    con.text_factory = str
    c   = con.cursor()
    return c, con

def db_create(c, con):
    # check if the table exists
    try:
        c.execute("SELECT * FROM Quotes")
    except lite.OperationalError:
        print "Creating Table Quotes"
        c.execute("CREATE TABLE Quotes(quote text, source text)")
        con.commit()

def add_quote(quote, source, c, con):
    c.execute("INSERT INTO Quotes(quote, source) values(?, ?)", (quote, source))
    con.commit()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

c, con = db_connect()
db_create(c, con)


for page_no in xrange(16, 45):
        print page_no,
        try :
            req = urllib2.Request(URL % page_no)
            req.add_header('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11')
            html_page = urllib2.urlopen(req)
        except urllib2.URLError as reason :
            print("URLError : %s" % (reason,), 2)
            continue
        except  ValueError :
            print("Invalid URL : %s" % current_url, 2)
            continue
        source = html_page.read()
        soup = BeautifulSoup(source, fromEncoding="utf-8")
        quotes_divs = soup.findAll(attrs={'class': 'quotesDiv'})
        for quote_div in quotes_divs:
            source = quote_div.findAll('p')[0]
            quote  = quote_div.findAll('p')[1]
            source = strip_tags(str(source))
            quote = strip_tags(str(quote))
            add_quote(quote, source, c, con)
