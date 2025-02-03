"""
DbTransfer_5.py

This script will:
  - Import the final structured/validated data (e.g., `validDict`) from MLModelReturns_4.py
  - Connect to a MySQL database
  - Insert each record into a table (e.g., `news`) with columns: (title, summary, link, published, topic).

Students:
 - Fill out the pseudo code to connect to the DB, handle potential errors,
   and insert data in a loop or with executemany.
"""

# from MLModelReturns_4 import validDict
import json
import mysql.connector
import MLModelReturns_4
validDict = MLModelReturns_4.main()

DB_CONFIG = {
    "host": "localhost",  # Uppdatera om MySQL är på en annan server
    "user": "JonHemdator",  # Uppdatera med din MySQL-användare
    "password": "jTc5r3pQcCctB#esWc2&",  # Uppdatera med ditt lösenord
    "database": "ml_project"  # Databasnamnet du skapade
}

def db_connection():
    """ Skapar och returnerar en databasanslutning. """
    try:
        cnxn = mysql.connector.connect(**DB_CONFIG)
        print("Databasanslutning lyckades!")
        return cnxn
    except mysql.connector.Error as err:
        print(f"Fel vid anslutning: {err}")
        return None

def insert_data(data, cnxn):
    """ Infogar artikeldatan i MySQL-tabellen 'news'. """
    cursor = cnxn.cursor()
    sql = """
    INSERT INTO news (title, summary, link, published, topic)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    values = [(d["title"], d["summary"], d["link"], d["published"], json.dumps(d["categories"])) for d in data]
    
    try:
        cursor.executemany(sql, values)
        cnxn.commit()
        print(f"{cursor.rowcount} rader infogade i databasen.")
    except mysql.connector.Error as err:
        print(f"Fel vid infogning: {err}")
    finally:
        cursor.close()

def calculate_category_counts(cnxn):
    """ Räknar antal artiklar per kategori och lagrar i databasen """
    cursor = cnxn.cursor()

    # Hämta kategoriantal
    cursor.execute("SELECT topic FROM news")
    topics = cursor.fetchall()

    category_count = {}
    for row in topics:
        categories = json.loads(row[0])  # Konvertera JSON-sträng till lista
        for category in categories:
            category_count[category] = category_count.get(category, 0) + 1

    # Infoga eller uppdatera kategoriantal i databasen
    cursor.execute("DELETE FROM category_counts")  # Rensa tabellen först
    insert_query = "INSERT INTO category_counts (category, article_count) VALUES (%s, %s)"
    cursor.executemany(insert_query, list(category_count.items()))

    cnxn.commit()
    cursor.close()


def main():
    cnxn = db_connection()
    if cnxn:
        insert_data(validDict, cnxn)  # Infoga artiklar i databasen
        calculate_category_counts(cnxn)  # Beräkna kategoriantal
        cnxn.close()
        print("Databasanslutning stängd.")
    else:
        print("Ingen databasanslutning etablerad.")

if __name__ == "__main__":
    main()

