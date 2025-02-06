import datetime

# Import the `posts` from another script
from RssArticles_1_Ulf import posts

# Check the number of articles in posts.
print(f"Number of articles in posts: {len(posts)}")

def getting_necessary_list():
    """
    Loops through 'posts' and extracts:
    - title, summary, link, and published.
    Returns a list of dictionaries containing these fields.
    """
    all_items = []
    for post in posts:
        try:
            temp_dict = {
                "title": post.get("title", ""),  # Get the title or default to an empty string.
                "summary": post.get("summary", ""),  # Get the summary or default to an empty string.
                "link": post.get("link", ""),  # Get the link or default to an empty string.
                "published": post.get("published", "")  # Get the published date or default to an empty string.
            }
            all_items.append(temp_dict)
        except Exception as e:
            print(f"Error processing post: {e}")
    return all_items

# Extract the necessary data.
all_items = getting_necessary_list()
print(all_items[:5])  # Print the first five entries to preview the data.
print(len(all_items))  # Print the total number of items.

def parse_date(date_str):
    """
    Attempts to parse a date string using various formats and returns it in the standard format 'YYYY-MM-DD HH:MM:SS'.
    If parsing fails, raises a ValueError to flag the issue.
    """
    date_formats = [
        "%a, %d %b %Y %H:%M:%S %z",  # Example: "Mon, 03 Feb 2025 10:20:30 +0100"
        "%a, %d %b %Y %H:%M:%S GMT",  # Example: "Mon, 03 Feb 2025 10:20:30 GMT"
    ]
    for fmt in date_formats:
        try:
            # Try to parse the date with one of the formats.
            date_obj = datetime.datetime.strptime(date_str, fmt)
            return date_obj.strftime("%Y-%m-%d %H:%M:%S")  # Convert to standard format.
        except ValueError:
            continue
    
    # Raise an error if all formats fail.
    raise ValueError(f"Unknown date format: {date_str}")

def the_final_list():
    """
    Converts the list from 'getting_necessary_list()' into the final list.
    Formats the 'published' date field into the standard format.
    """
    all_items = getting_necessary_list()
    final_list = []

    for item in all_items:
        try:
            # Parse and format the published date.
            published_date = item["published"]
            published_str = parse_date(published_date)

            # Append the formatted item to the final list.
            final_list.append([item["title"], item["summary"], item["link"], published_str])
        except Exception as e:
            print(f"Error processing article: {item}, Error: {e}")

    print(f"Number of articles in the final list: {len(final_list)}")
    return final_list

# Generate the final list.
my_final_list = the_final_list()

# Output the results.
print(f"Total articles: {len(my_final_list)}")
print(f"Final list: {my_final_list[:5]}")  # Display the first five entries for review.

# Print each article in a readable format.
for item in my_final_list[:5]:
    print(f"Title: {item[0]}")
    print(f"Summary: {item[1]}")
    print(f"Link: {item[2]}")
    print(f"Published: {item[3]}")
    print("---")




