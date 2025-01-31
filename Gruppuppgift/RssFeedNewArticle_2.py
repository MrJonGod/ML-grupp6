# This scripts receives the posts (Rss extracted news articles from the NEWRsArticles.py file)
# it is then cleans and structures them to be imported by NEWMLModelMLC.py

# Import packages/files
from RssArticles_1 import posts

"""
import feedparser

# This function can be used if from NEWRssArticles import posts is not desired
################################ RSS FEED Parser #####################################

RSS_URLS = ['http://www.dn.se/nyheter/m/rss/',
            'https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/', 'https://feeds.expressen.se/nyheter/',
            'http://www.svd.se/?service=rss', 'http://api.sr.se/api/rss/program/83?format=145',
            'http://www.svt.se/nyheter/rss.xml'
              ]

posts = []

for url in RSS_URLS:
    posts.extend(feedparser.parse(url).entries)

######################################################################################

print(posts)





##################### Extracting the titles and summeries from the dataset ##################

def OnlyTitlesandSumaries():
    only_titles_and_summaries = []
    for x in posts:
        try:
            tempdict = {}
            tempdict["title"] = x["title"]
            tempdict["summary"] = x["summary"]
            only_titles_and_summaries.append(tempdict)
        except KeyError as ke:
            only_titles_and_summaries.append("") #replace the missing keys with empty space
    return only_titles_and_summaries

Only_the_titles_Summaries = OnlyTitlesandSumaries()


def TitleAndSummaryList():
    title_and_summary_list = []
    temp_and_summary_title_list = []
    for x in Only_the_titles_Summaries:
        for key in x:
            if 'title' == key:
                firstkey = x[key]
            if 'summary' == key:
                secondkey = x[key]
                temp_and_summary_title_list.append(firstkey + ' ' + secondkey)
        title_and_summary_list.append(temp_and_summary_title_list)
        temp_and_summary_title_list = []
    return title_and_summary_list

The_Title_Summary_List = TitleAndSummaryList()


#print(The_Title_Summary_List)
######################################################################################



##################### Concatenating the list of Titles into a single list  ##################

def PrintDeposit():
    newList= []
    for item in The_Title_Summary_List:
        for value in item:
            newList.append(value)
    return newList

printdepositlist = PrintDeposit()

print(printdepositlist)

######################################################################################

"""

# ------------------------------------------------------------------
# student_solution.py
# ------------------------------------------------------------------
# Purpose: Demonstration of data preprocessing steps on RSS feed data.
#          We'll extract the 'title' and 'summary' from each news article,
#          handle missing keys by assigning empty strings, combine them,
#          and finally flatten the combined results into a single list.
# ------------------------------------------------------------------

# ----------------------
# 1. Import the posts
# ----------------------
# We assume you have a Python file named RssArticles_1.py containing 
# a variable called 'posts'. Each element in 'posts' is typically 
# a dictionary returned by the feedparser.
# For instance: 
#   posts = [
#       {
#           "title": "News Title 1",
#           "summary": "News summary details here ..."
#       },
#       {
#           "title": "News Title 2",
#           "summary": "Another summary ..."
#       },
#       ...
#   ]
#
# The line below imports that 'posts' object.
from RssArticles_1 import posts


def OnlyTitlesandSummaries():
    """
    This function loops through the global 'posts' and extracts only
    the 'title' and 'summary' from each item. If a key doesn't exist,
    it replaces it with an empty string ("").
    
    Returns:
        only_titles_and_summaries (list): A list of dictionaries, where
        each dictionary has the keys 'title' and 'summary' only.
    """
    # Initialize an empty list that will hold our cleaned dictionaries
    only_titles_and_summaries = []
    
    # Loop through each item in the 'posts' list
    for x in posts:
        
        # Create a temporary dictionary to store 'title' and 'summary'
        tempdict = {}
        
        # Attempt to read the 'title'; if missing, store empty string
        try:
            tempdict["title"] = x["title"]
        except KeyError:
            tempdict["title"] = ""
        
        # Attempt to read the 'summary'; if missing, store empty string
        try:
            tempdict["summary"] = x["summary"]
        except KeyError:
            tempdict["summary"] = ""
        
        # Append the tempdict to our main list once both fields are processed
        only_titles_and_summaries.append(tempdict)
    
    # Return the final list, which now only has 'title' and 'summary' keys
    return only_titles_and_summaries


def TitleAndSummaryList(only_titles_and_summaries):
    """
    This function takes a list of dictionaries (each containing 'title' 
    and 'summary') and creates a nested list, where each inner list has 
    exactly one combined string: "title summary".
    
    Args:
        only_titles_and_summaries (list): List of dictionaries 
                                          (each has 'title' and 'summary').

    Returns:
        title_and_summary_list (list): A nested list where each sub-list 
                                       contains a single combined string.
    """
    # Initialize an empty list that will hold nested lists
    title_and_summary_list = []
    
    # Loop through each dictionary in the provided list
    for item in only_titles_and_summaries:
        # Combine the title and summary into one string
        combined = item["title"] + " " + item["summary"]
        
        # Append the combined text as a single-element list
        title_and_summary_list.append([combined])
    
    # Return the nested list
    return title_and_summary_list


def PrintDeposit(title_and_summary_list):
    """
    This function flattens the nested list returned by TitleAndSummaryList. 
    Each sub-list might look like ["Title Summary"], and we want a single 
    one-dimensional list like ["Title Summary", "Another Title Summary", ...].
    
    Args:
        title_and_summary_list (list): Nested list of single-element lists 
                                       containing "title summary" strings.

    Returns:
        flattened_list (list): A one-dimensional list of combined strings.
    """
    # Initialize an empty list to hold our flattened strings
    flattened_list = []
    
    # Loop through each sub-list in the nested list
    for item in title_and_summary_list:
        
        # Each 'item' itself might be something like ["Title Summary"]
        for value in item:
            # Add each string to our flattened_list
            flattened_list.append(value)
    
    # Return the flattened list of strings
    return flattened_list


# 1. Extract only the 'title' and 'summary' keys (handling missing ones)
Only_the_titles_Summaries = OnlyTitlesandSummaries()
    
# 2. Build a nested list combining the title and summary into one string
The_Title_Summary_List = TitleAndSummaryList(Only_the_titles_Summaries)
    
# 3. Flatten the nested list into a single list of strings
printdepositlist = PrintDeposit(The_Title_Summary_List)


# -------------------- MAIN EXECUTION SECTION --------------------
if __name__ == "__main__":
   # 4. Print to verify the results
    print(printdepositlist)
