import streamlit as st
import mysql.connector
import json
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# Databasuppkoppling
DB_CONFIG = {
    "host": "localhost",
    "user": "JonHemdator",
    "password": "jTc5r3pQcCctB#esWc2&",
    "database": "ml_project"
}

def fetch_data():
    """ Hämtar artiklar från MySQL-databasen """
    cnxn = mysql.connector.connect(**DB_CONFIG)
    cursor = cnxn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM news ORDER BY published DESC")
    rows = cursor.fetchall()
    cursor.close()
    cnxn.close()
    return rows

def fetch_category_counts():
    """ Hämtar kategoriantal från MySQL """
    cnxn = mysql.connector.connect(**DB_CONFIG)
    cursor = cnxn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM category_counts")
    data = cursor.fetchall()
    cursor.close()
    cnxn.close()
    return data

def generate_wordcloud():
    """ Skapar ett Word Cloud från artikeltexter """
    cnxn = mysql.connector.connect(**DB_CONFIG)
    cursor = cnxn.cursor(dictionary=True)
    cursor.execute("SELECT summary FROM news")
    summaries = cursor.fetchall()
    cursor.close()
    cnxn.close()

    text = " ".join([row["summary"] for row in summaries])
    
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    return fig

def generate_bar_chart():
    """ Genererar en barchart med kategoriantal """
    category_data = fetch_category_counts()
    if category_data:
        df = pd.DataFrame(category_data)
        fig, ax = plt.subplots(figsize=(8, 5))
        df.set_index("category").plot(kind="bar", ax=ax, legend=False, color="skyblue")
        ax.set_title("Antal artiklar per kategori")
        ax.set_ylabel("Antal artiklar")
        ax.set_xlabel("Kategori")
        plt.xticks(rotation=45, ha="right")
        return fig
    else:
        return None

def main():
    st.set_page_config(page_title="Nyhetsflöde", layout="wide")

    st.sidebar.title("📌 Navigering")
    page = st.sidebar.radio("Välj en vy:", ["📰 Nyhetsartiklar", "📊 Dataanalys"])

    if page == "📰 Nyhetsartiklar":
        st.title("📰 AI-Klassificerade Nyhetsartiklar")
        st.write("Här kan du se nyhetsartiklar klassificerade av vår ML-modell.")

        # Hämta artiklar
        data = fetch_data()

        # Skapa en lista med unika kategorier
        unique_categories = set()
        for row in data:
            categories = json.loads(row["topic"])
            unique_categories.update(categories)
        unique_categories = sorted(unique_categories)

        # Filtreringsalternativ i sidomenyn
        selected_category = st.sidebar.selectbox("📂 Filtrera efter kategori:", ["Alla"] + unique_categories)
        search_query = st.sidebar.text_input("🔍 Sök efter artiklar")

        # Filtrera data baserat på användarens val
        filtered_data = data
        if selected_category != "Alla":
            filtered_data = [row for row in filtered_data if selected_category in json.loads(row["topic"])]
        if search_query:
            filtered_data = [row for row in filtered_data if search_query.lower() in row['title'].lower() or search_query.lower() in row['summary'].lower()]

        # Visa filtrerade artiklar
        for row in filtered_data:
            with st.container():
                st.subheader(row['title'])
                st.write(row['summary'])
                st.write(f"🕒 Publicerad: {row['published']}")
                st.write(f"🏷 Kategorier: {', '.join(json.loads(row['topic']))}")
                st.markdown(f"[🔗 Läs mer]({row['link']})")
                st.write("---")

    elif page == "📊 Dataanalys":
        st.title("📊 Dataanalys av Artiklar")
        st.write("Här kan du analysera datasetet baserat på kategorier och innehåll.")

        # Bar chart
        st.subheader("🔹 Antal artiklar per kategori")
        bar_chart = generate_bar_chart()
        if bar_chart:
            st.pyplot(bar_chart)
        else:
            st.write("Ingen data att visa.")

        # Word Cloud
        st.subheader("🔹 Vanliga ord i nyhetsartiklar")
        wordcloud_fig = generate_wordcloud()
        st.pyplot(wordcloud_fig)

if __name__ == "__main__":
    main()
