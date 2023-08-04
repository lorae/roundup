# Fed_Atlanta.py
# The purpose of this script is to scrape metadata from the most recent Atlanta Fed working papers. This script uses
# the Atlanta Fed's RSS feed. 
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 1 Aug 2023
import feedparser
import pandas as pd
import calendar

# I define the function "scrape" in every webscraper. That way, in runall.py, it is easy to call BOE.scrape()
# or NBER.scrape(), for instance, knowing that they all do the same thing - namely, navigate to their respective 
# websites and extract the data.
def scrape():
    url = "https://www.atlantafed.org/rss/wps"
    f = feedparser.parse(url)
       
    Title = []
    Link = []
    Date = []
    Abstract = []
    Number = []
    Author = []

    for entry in f.entries:
        # Get the title
        Title.append(entry.title)
        
        # Get the link
        Link.append(entry.link)
        
        # The date is the published entry, minus 11 characters (indicating hour, minute, and time zone)
        date = entry.published[:-11].strip()
        # The last 4 chars of date comprise the year (helper variable)
        year = date[-4:] # year is a helper variable
        mon = date[-8:-5] # mon is a helper variable (3-letter month name)
        month_year = calendar.month_name[list(calendar.month_abbr).index(mon)] + " " + year # helper variable
        Date.append(date)
        
        # The abstract is the 1st element of "description", after splitting it by the name of the month and year
        # the paper was published. This is because the "desciption" also contains author and working 
        # paper number. This was the simplest way I could find to isolate the abstract without navigating
        # to different URLs.
        Abstract.append(entry.description.split(f"{month_year}")[1])
        
        # The number is the middle element of "description", after splitting it by the string "Working Paper" and
        # by the month_year string.
        number = entry.description.split("Working Paper ")[1].split(f"{month_year}")[0].strip()
        Number.append(number)
        
        # The author is the first element of "description", the part that appears just before the string "Working Paper".
        Author.append(entry.description.split("Working Paper")[0].strip())
       
    # Create a dictionary of the six lists, where the keys are the column names.
    data = {'Title': Title,
            'Link': Link,
            'Date': Date,
            'Author': Author,
            'Number': Number,
            'Abstract': Abstract}

    # Create a DataFrame from the dictionary.
    df = pd.DataFrame(data)
    
    # Instead of the data frame having row names (indices) equalling 1, 2, etc,
    # we set them to be an identifier that is unique. In the case of Chicago, we combine
    # Chicago with the number of the paper (eg. 999) to get an identifier Chicago999 that
    # is completely unique across all papers scraped.
    df["Source"] = "FED-ATLANTA"
    df.index = df["Source"] + df['Number'].astype(str)
    df.index.name = None
        
    print(df)
    return(df)


# Create a pandas data frame from the extracted data



'''
# Extract the HTML content for each link in the data frame using the get_element() function
elements = get_element(df)

# Extract the abstracts, authors, and numbers for each HTML tree using get_abstracts, get_authors,
# and get_numbers
df["Abstract"] = get_abstracts(elements)
#print("... abstracts have been gathered.")
df["Author"] = get_authors(elements)
#print("... authors have been gathered.")
df["Number"] = get_numbers(elements)
#print("... numbers have been gathered.")

# Instead of the data frame having row names (indices) equalling 1, 2, etc,
# we set them to be an identifier that is unique. In the case of Chicago, we combine
# Chicago with the number of the paper (eg. 999) to get an identifier Chicago999 that
# is completely unique across all papers scraped.
df["Source"] = "IMF"
df.index = df["Source"] + df['Number'].astype(str)
df.index.name = None

print(df)
#return(df)
'''
