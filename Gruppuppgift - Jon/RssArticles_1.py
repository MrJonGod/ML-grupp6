# Import packages
import feedparser

# Define RSS feed URLs
RSS_URLS = [
    'https://www.dn.se/rss/',
    'https://www.svt.se/rss.xml',
    'https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/'
]

# Create an empty list for posts
posts = []

# Loop through each RSS feed URL and extend the posts list with entries
for url in RSS_URLS:
    posts.extend(feedparser.parse(url).entries)