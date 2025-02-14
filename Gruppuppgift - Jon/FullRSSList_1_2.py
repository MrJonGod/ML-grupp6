"""
FullRSSList_1_2.py

This script takes in articles (posts) from RssArticles_1.py (via `posts`),
extracts the desired fields (title, summary, link, and published),
fixes data format issues (like dates), and provides the final list as 'MyTheFinalList'.

"""

# Import posts from RssArticles_1
from RssArticles_1 import posts
import datetime

def gettingNecessaryList():
    """
    This function loops through 'posts' and extracts:
      title, summary, link, published
    Then stores them in a dictionary, finally returns a list of these dictionaries.
    """
    allitems = []
    
    for post in posts:
        try:
            tempdict = {}
            tempdict["title"] = post["title"]
        except KeyError:
            tempdict["title"] = ""

        try:
            tempdict["summary"] = post["summary"]
        except KeyError:
            tempdict["summary"] = ""

        try:
            tempdict["link"] = post["link"]
        except KeyError:
            tempdict["link"] = ""

        try:
            tempdict["published"] = post["published"]
        except KeyError:
            tempdict["published"] = ""

        allitems.append(tempdict)

    return allitems


# Store the list of extracted items
AllItemsX = gettingNecessaryList()


def ThefinalList():
    """
    This function converts AllItemsX into a final 2D list (or list of lists),
    while ensuring that 'published' is properly formatted (YYYY-MM-DD HH:MM:SS).
    """
    
    finalList = []
    
    for item in AllItemsX:
        title = item["title"]
        summary = item["summary"]
        link = item["link"]
        published = item["published"]
        try:
            published = datetime.datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            try:
                published = datetime.datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %Z")
            except ValueError:
                try:
                    published = datetime.datetime.strptime(published, "%a, %d %b %Y %H:%M:%S")
                except ValueError:
                    try:
                        published = datetime.datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")
                    except ValueError:
                        published = datetime.datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %Z")
        published_str = published.strftime("%Y-%m-%d %H:%M:%S")
        
        finalList.append([title, summary, link, published_str])
        
    return finalList
    

# Create a variable that holds the final list
MyTheFinalList = ThefinalList()

print(MyTheFinalList)
print(len(MyTheFinalList))