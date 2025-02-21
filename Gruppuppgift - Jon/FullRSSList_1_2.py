"""
FullRSSList_1_2.py

This script processes articles (posts) from RssArticles_1.py.
It extracts key fields (title, summary, link, and published),
formats dates into a consistent format, and returns a structured final list.

"""

# Import posts from RssArticles_1
from RssArticles_1 import posts
import datetime

def extract_rss_fields(posts):
    """
    Extracts necessary fields (title, summary, link, published) from RSS posts.
    Handles missing keys by returning empty strings.

    Args:
        posts (list): List of RSS feed entries.

    Returns:
        list: A list of dictionaries with extracted fields.
    """
    extracted_items = []
    
    for post in posts:
        extracted_items.append({
            "title": post.get("title", ""),
            "summary": post.get("summary", ""),
            "link": post.get("link", ""),
            "published": post.get("published", "")
        })

    return extracted_items


def format_rss_data(items):
    """
    Converts extracted RSS data into a structured 2D list.
    Ensures 'published' field is formatted as 'YYYY-MM-DD HH:MM:SS'.

    Args:
        items (list): List of dictionaries containing extracted RSS fields.

    Returns:
        list: A list of lists with formatted RSS data.
    """
    
    date_formats = [
        "%a, %d %b %Y %H:%M:%S %z",  # Example: Mon, 01 Jan 2024 12:30:00 +0000
        "%a, %d %b %Y %H:%M:%S %Z",  # Example: Mon, 01 Jan 2024 12:30:00 GMT
        "%a, %d %b %Y %H:%M:%S"      # Example: Mon, 01 Jan 2024 12:30:00
    ]
    
    formatted_list = []
    
    for item in items:
        title = item["title"]
        summary = item["summary"]
        link = item["link"]
        published = item["published"]
        
        # Try to parse date using different formats
        parsed_date = None
        for fmt in date_formats:
            try:
                parsed_date = datetime.datetime.strptime(published, fmt)
                break
            except ValueError:
                continue
        
        # If parsing fails, set default timestamp
        if not parsed_date:
            parsed_date = datetime.datetime(1970, 1, 1)  # Fallback date
        
        published_str = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        
        formatted_list.append([title, summary, link, published_str])
    
    return formatted_list

# Process RSS posts
extracted_posts = extract_rss_fields(posts)
MyTheFinalList = format_rss_data(extracted_posts)

# Print results
print(MyTheFinalList)
print(f"Total articles processed: {len(MyTheFinalList)}")