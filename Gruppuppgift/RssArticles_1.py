"""
RssArticles_1.py

This Python script retrieves and parses RSS feeds from three Swedish news 
sources (Dagens Nyheter, SVT, and Aftonbladet) using the feedparser library. 
It iterates through the provided RSS URLs, extracts the news entries from each 
feed, and stores them in a list called `posts`, which can be imported into 
other scripts.

"""

import feedparser

# Define RSS feed URLs
RSS_URLS = [
    'https://www.dn.se/rss/',
    'https://www.svt.se/rss.xml',
    'https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/'
]

def fetch_rss_feeds(urls):
    """
    Fetch and parse RSS feeds from a list of URLs.

    Args:
        urls (list): List of RSS feed URLs.

    Returns:
        list: A list containing all RSS feed entries.
    """
    posts = []
    for url in urls:
        try:
            feed = feedparser.parse(url)
            if feed.bozo:  # bozo attribute indicates a parsing error
                print(f"Warning: Could not parse feed from {url}")
                continue
            posts.extend(feed.entries)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    return posts

# Store the fetched posts in a variable that can be imported
posts = fetch_rss_feeds(RSS_URLS)

# Run as a script and print the number of articles when executed directly
if __name__ == "__main__":
    print(f"Retrieved {len(posts)} articles.")
