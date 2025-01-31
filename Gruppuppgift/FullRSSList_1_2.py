"""
FullRSSList_1_2.py

This script takes in articles (posts) from RssArticles_1.py (via `posts`),
extracts the desired fields (title, summary, link, and published),
fixes data format issues (like dates), and provides the final list as 'MyTheFinalList'.

Students: 
 - Ensure your 'RssArticles_1.py' is in the same folder (or adjust imports accordingly).
 - Examine how 'posts' is structured, and fix any date format issues carefully.
"""

# 1) Import posts from RssArticles_1
# from RssArticles_1 import posts
import datetime

# Pseudo code: 
# - create a function 'gettingNecessaryList' that loops through posts
# - extract title, summary, link, published
# - handle errors with try/except if fields are missing
# - return the collected list

def gettingNecessaryList():
    """
    This function loops through 'posts' and extracts:
      title, summary, link, published
    Then stores them in a dictionary, finally returns a list of these dictionaries.
    """
    # Pseudo code:
    #  1. Initialize an empty list (allitems)
    #  2. Loop through each 'post' in 'posts'
    #  3. Create a temp dict for each 'post'
    #  4. Extract needed keys; if missing, set to empty string
    #  5. Append the dict to the list
    #  6. Return allitems
    
    allitems = []
    
    # TODO: Replace with your actual code, e.g.:
    # for x in posts:
    #     try:
    #         tempdict = {}
    #         tempdict["title"] = x["title"]
    #         tempdict["summary"] = x["summary"]
    #         ...
    #     except:
    #         ...
    #     ...
    
    return allitems


# 2) Store the list of extracted items
AllItemsX = gettingNecessaryList()


def ThefinalList():
    """
    This function converts AllItemsX into a final 2D list (or list of lists),
    while ensuring that 'published' is properly formatted (YYYY-MM-DD HH:MM:SS).
    """
    # Pseudo code:
    #  1. Initialize finalList = []
    #  2. For each item (dict) in AllItemsX:
    #       a) Extract title, summary, link, published
    #       b) Parse 'published' date with multiple possible formats
    #       c) Append results as a small list [title, summary, link, published_str] to finalList
    #  3. Return finalList
    
    finalList = []

    # TODO: Replace with your code that:
    # - loops over AllItemsX
    # - handles date parsing with datetime.strptime
    # - appends the processed items to finalList
    
    return finalList


# 3) Create a variable that holds the final list
MyTheFinalList = ThefinalList()


print(MyTheFinalList)
print(len(MyTheFinalList))