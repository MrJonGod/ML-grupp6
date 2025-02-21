"""
DbTransfer_5.py

This script transfers the classified and validated news articles to a MySQL database.
It:
  - Imports the structured data (`validDict`) from MLModelReturns_4.py
  - Establishes a connection to a MySQL database
  - Inserts only new articles into the `news` table, ensuring no duplicates using SQL constraints
  - Updates the `category_counts` table with the number of articles per category
"""

import json
import mysql.connector
import MLModelReturns_4
validDict = MLModelReturns_4.main()

# Database configuration - Update credentials as needed
DB_CONFIG = {
    "host": "localhost",  # Change if MySQL is hosted on a different server
    "user": "JonHemdator",  # Update with your MySQL username
    "password": "jTc5r3pQcCctB#esWc2&",  # Update with your MySQL password
    "database": "ml_project"  # Database name
}

def db_connection():
    """
    Establishes and returns a MySQL database connection.
    """
    try:
        cnxn = mysql.connector.connect(**DB_CONFIG)
        print("Database connection successful!")
        return cnxn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def insert_data(data, cnxn):
    """
    Inserts classified articles into the `news` table, avoiding duplicates using SQL's ON DUPLICATE KEY UPDATE.
    """
    cursor = cnxn.cursor()
    sql = """
    INSERT INTO news (title, summary, link, published, topic)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE title = VALUES(title), summary = VALUES(summary), published = VALUES(published), topic = VALUES(topic);
    """
    
    values = [(d["title"], d["summary"], d["link"], d["published"], json.dumps(d["categories"])) for d in data]
    
    try:
        cursor.executemany(sql, values)
        cnxn.commit()
        print(f"{cursor.rowcount} articles processed (newly inserted or updated in the database).")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()

def calculate_category_counts(cnxn):
    """
    Counts the number of articles per category and updates the `category_counts` table.
    """
    cursor = cnxn.cursor()

    # Retrieve all categories from the news table
    cursor.execute("SELECT topic FROM news")
    topics = cursor.fetchall()

    category_count = {}
    for row in topics:
        categories = json.loads(row[0])  # Convert JSON string to list
        for category in categories:
            category_count[category] = category_count.get(category, 0) + 1

    # Clear the category_counts table before updating
    cursor.execute("DELETE FROM category_counts")
    insert_query = "INSERT INTO category_counts (category, article_count) VALUES (%s, %s)"
    cursor.executemany(insert_query, list(category_count.items()))

    cnxn.commit()
    cursor.close()

def main():
    """
    Main function to connect to the database, insert or update news articles, and update category counts.
    """
    cnxn = db_connection()
    if cnxn:
        insert_data(validDict, cnxn)  # Insert or update news articles in the database
        calculate_category_counts(cnxn)  # Update category counts
        cnxn.close()
        print("Database connection closed.")
    else:
        print("No database connection established.")

if __name__ == "__main__":
    main()


"""
Database connection successful!
174 articles processed (newly inserted or updated in the database).
Database connection closed.
"""