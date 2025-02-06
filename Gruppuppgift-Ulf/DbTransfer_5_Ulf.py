import json
import mysql.connector
import MLModelReturns_4_Ulf
from MLModelReturns_4_Ulf import validDict

from dotenv import load_dotenv
import os

# Ladda miljövariabler från .env-filen
load_dotenv()


print(f"validDict innehåller {len(validDict)} artiklar.")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}
print("DB_CONFIG:", DB_CONFIG)

# Kontroll för att säkerställa att alla variabler är korrekt laddade
if not all(DB_CONFIG.values()):
    raise ValueError("Alla miljövariabler är inte korrekt definierade i .env-filen.")

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

    # Rensa tabellen och infoga kategoriantal
    cursor.execute("DELETE FROM category_counts")
    insert_query = "INSERT INTO category_counts (category, article_count) VALUES (%s, %s)"
    cursor.executemany(insert_query, list(category_count.items()))

    cnxn.commit()
    cursor.close()
    print("Kategoriantal har uppdaterats.")

def main():
    cnxn = db_connection()
    if cnxn:
        insert_data(validDict, cnxn)  # Infoga artiklar i databasen
        calculate_category_counts(cnxn)  # Uppdatera kategoriantal
        cnxn.close()
        print("Databasanslutning stängd.")
    else:
        print("Ingen databasanslutning etablerad.")

if __name__ == "__main__":
    main()
