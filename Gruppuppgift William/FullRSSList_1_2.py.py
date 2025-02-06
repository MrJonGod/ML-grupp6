"""
FullRSSList_1_2.py

This script retrieves articles from 'RssArticles_1william.py' (via `posts`),
extracts the required fields (tiitle, summary, link, and published),
corrects date formatting issues, and generates 'MyTheFinalList' containing the formatted data.

Students:
 - Ensure your 'RssArticles_1william.py' is in the same directory (or adjust the import path).
 - Investigate the structure of 'posts' and carefully adjust any date format issues.
"""

# 1) Import posts from RssArticles_1william
from RssArticles_1william import posts
import datetime

def extractPostData():
    """
    Loops through each post in 'posts', extracts necessary fields,
    and manages missing data with default values.
    """
    extracted_data = []
    for post in posts:
        data_dict = {
            "title": post.get("title", "No title provided"),
            "summary": post.get("summary", "No summary available"),
            "link": post.get("link", "No link available"),
            "published": post.get("published", "No date provided")
        }
        extracted_data.append(data_dict)
    return extracted_data

# Store the extracted data
extractedItems = extractPostData()

def formatPostData():
    """
    Converts the list of dictionaries into a formatted list,
    ensuring the 'published' date is standardized to 'YYYY-MM-DD HH:MM:SS'.
    """
    formatted_list = []
    for item in extractedItems:
        date_string = item["published"]
        try:
            formatted_date = datetime.datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            formatted_date = datetime.datetime.now()  # Fallback to current date/time if parsing fails
        formatted_date_str = formatted_date.strftime("%Y-%m-%d %H:%M:%S")
        formatted_list.append([item["title"], item["summary"], item["link"], formatted_date_str])
    return formatted_list

# Generate the final list
MyTheFinalList = formatPostData()

print(MyTheFinalList)
print("Total items formatted:", len(MyTheFinalList))
