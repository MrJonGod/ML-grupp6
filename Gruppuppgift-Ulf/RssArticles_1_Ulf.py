# Defining the RSS URL:s for Svenska Dagbladet, Barometern, Borås Tidningar
import feedparser

RSS_URLS = [
    'https://www.barometern.se/feed',
    'https://www.svd.se/feed/articles.rss',
    'https://www.bt.se/feed'
]

# Create an empty list, posts, to store alla feeds.

posts = []

# Loop through each RSS feed URL and extend the posts list with entries
for url in RSS_URLS:
    posts.extend(feedparser.parse(url).entries)

    
print(len(posts))

