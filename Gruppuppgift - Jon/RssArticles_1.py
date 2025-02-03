# Import packages
import feedparser

# Define RSS feed URLs
RSS_URLS = [
    'https://www.dn.se/rss/',
    'https://www.svt.se/nyheter/lokalt/skane/rss.xml',
    'https://polisen.se/aktuellt/rss/skane/nyheter-rss---skane/'
]

# Create an empty list for posts
posts = []

# Loop through each RSS feed URL and extend the posts list with entries
for url in RSS_URLS:
    posts.extend(feedparser.parse(url).entries)