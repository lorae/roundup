# Lorae Stojanovic
# LE: 21 Nov 2022
# https://realpython.com/beautiful-soup-web-scraper-python/
import requests
from beautifulsoup4 import BeautifulSoup
import feedparser
import pandas as pd # for data frame
#from itertools import compress # for compress function

'''
Everything but the abstract and authors are in the RSS feed, so to simplify
life  we'll get all of that data directly from the feed.
"Sum" and "Use" are only temporarily needed to indicate which parts
of the RSS feed are working papers and which are other things (quarterly
reports, etc))
'''
URL = "https://www.bankofengland.co.uk/rss/publications"
f = feedparser.parse(URL)
Title = []
Link = []
Date = []
Sum = []
Use = []
for n in range(0, len(f.entries)):
    title = (f.entries[n].title)
    link = (f.entries[n].link)
    sum = (f.entries[n].summary)
    pub_date = (f.entries[n].published)
    if "working paper" in sum:
        Use.append(True)
    else:
        Use.append(False)
    Title.append(title)
    Link.append(link)
    Sum.append(sum)
    Date.append(pub_date)
'''
Now we've extracted titles and links. To use only the links that say 
"working-paper" in their URL, we'll use the compress() function.
'''
def choose(x, use):
    output = list(compress(x, use))
    return output

Title = choose(Title, Use)
Link = choose(Link, Use)
Date = choose(Date, Use)

'''
Now we need the abstract and authors. For that, we have to individually
navigate to each link.
'''
#def get_abstract(url):
    #read url
    #extract entire container "div.page-content". Necessary since each container
    #is different
    #parse text,
    #split by "\n" marker
    #grab third element
#def get_author(url):
    #read url
    #extract entire container "div.page-content". Necessary since each container
    #is different
    #parse text,
    #split by "\n" marker
    #grab third element
Abstract = []
Author = []
for m in range(0, len(Link)):
    link = (Link[m])

print(Link[1])
# df1 = pd.DataFrame(lst, columns=cols)
# print(df1)

