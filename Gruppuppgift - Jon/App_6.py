"""
News Dashboard Application

This Streamlit application connects to a MySQL database to fetch, filter, and display AI-classified news articles.
It provides two main views:
    1. News Articles View: Lists news articles with filtering options.
    2. Data Analysis View: Displays visualizations including a bar chart, line chart, and word cloud.
The structure and commenting style is aligned with the MLModelReturns_4.py file.
"""

# Standard library imports
import json
import datetime

# Third-party imports
import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
import matplotlib.dates as mdates

# Download Swedish stopwords if not already available
nltk.download('stopwords')
SWEDISH_STOPWORDS = set(stopwords.words('swedish'))

# Database configuration using Streamlit secrets
DB_CONFIG = {
    "host": st.secrets["db_host"],
    "user": st.secrets["db_user"],
    "password": st.secrets["db_password"],
    "database": st.secrets["db_database"]
}

def get_db_connection():
    """
    Establishes and returns a MySQL database connection.
    
    Returns:
        mysql.connector.connection.MySQLConnection: The database connection object.
    """
    return mysql.connector.connect(**DB_CONFIG)

def fetch_articles():
    """
    Retrieves all news articles from the database, ordered by publication date (most recent first).
    
    Returns:
        list: A list of dictionaries representing news articles.
    """
    cnxn = get_db_connection()
    cursor = cnxn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM news ORDER BY published DESC")
    articles = cursor.fetchall()
    cursor.close()
    cnxn.close()
    return articles

def fetch_category_counts(start_date, end_date):
    """
    Retrieves the count of articles per category within the specified date range.
    
    Args:
        start_date (date): The start date for filtering articles.
        end_date (date): The end date for filtering articles.
    
    Returns:
        dict: A dictionary with category names as keys and counts as values.
    """
    cnxn = get_db_connection()
    cursor = cnxn.cursor(dictionary=True)
    query = """
    SELECT topic FROM news
    WHERE published BETWEEN %s AND %s
    """
    cursor.execute(query, (start_date, end_date))
    topics = cursor.fetchall()
    cursor.close()
    cnxn.close()

    category_count = {}
    for row in topics:
        # Parse the JSON string to obtain the list of categories
        categories = json.loads(row["topic"])
        for category in categories:
            category_count[category] = category_count.get(category, 0) + 1

    return category_count

def generate_wordcloud(start_date, end_date):
    """
    Generates a WordCloud visualization based on article summaries within the specified date range.
    
    Args:
        start_date (date): The start date for filtering articles.
        end_date (date): The end date for filtering articles.
    
    Returns:
        matplotlib.figure.Figure or None: The WordCloud figure if text exists; otherwise, None.
    """
    cnxn = get_db_connection()
    cursor = cnxn.cursor(dictionary=True)
    query = """
    SELECT summary FROM news
    WHERE published BETWEEN %s AND %s
    """
    cursor.execute(query, (start_date, end_date))
    summaries = cursor.fetchall()
    cursor.close()
    cnxn.close()

    # Combine summaries into a single text and remove stopwords
    text = " ".join([row["summary"] for row in summaries])
    cleaned_text = " ".join([word for word in text.split() if word.lower() not in SWEDISH_STOPWORDS])

    if cleaned_text.strip():
        wordcloud = WordCloud(width=800, height=400, background_color="#0E1117").generate(cleaned_text)
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor("#0E1117")
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        return fig
    else:
        return None

def generate_bar_chart(start_date, end_date):
    """
    Generates a horizontal bar chart showing the number of articles per category within a specified date range.
    
    Args:
        start_date (date): The start date for filtering articles.
        end_date (date): The end date for filtering articles.
    
    Returns:
        matplotlib.figure.Figure or None: The bar chart figure if data is available; otherwise, None.
    """
    category_data = fetch_category_counts(start_date, end_date)
    if category_data:
        df = pd.DataFrame(list(category_data.items()), columns=["Kategori", "Antal"])
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        
        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        df.set_index("Kategori").plot(kind="barh", ax=ax, legend=False, color="#4086DC")

        # Format y-tick labels
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=10, color="white", fontweight="bold")
        ax.set_ylabel("")
        ax.xaxis.set_visible(False)
        ax.tick_params(axis="y", which="both", left=False)

        # Remove axis spines for a cleaner look
        for spine in ax.spines.values():
            spine.set_visible(False)

        # Annotate each bar with its count
        for p in ax.patches:
            ax.annotate(f"{p.get_width():.0f}", 
                        (p.get_width() + 0.5, p.get_y() + p.get_height() / 2), 
                        ha="left", va="center", fontsize=10, color="white", fontweight="bold")
        return fig
    else:
        return None

def generate_line_chart(start_date, end_date):
    """
    Generates a line chart depicting the number of articles per category per day within the specified date range.
    
    Args:
        start_date (date): The start date for filtering articles.
        end_date (date): The end date for filtering articles.
    
    Returns:
        matplotlib.figure.Figure or None: The line chart figure if data is available; otherwise, None.
    """
    cnxn = get_db_connection()
    cursor = cnxn.cursor(dictionary=True)
    query = """
    SELECT DATE(published) AS publish_date, topic
    FROM news
    WHERE published BETWEEN %s AND %s
    """
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()
    cursor.close()
    cnxn.close()

    df = pd.DataFrame(data)
    if df.empty:
        return None

    # Expand JSON categories into separate rows
    exploded_data = []
    for _, row in df.iterrows():
        categories = json.loads(row["topic"])
        for category in categories:
            exploded_data.append({"publish_date": row["publish_date"], "category": category})
    df_expanded = pd.DataFrame(exploded_data)

    # Group data and pivot for plotting
    df_grouped = df_expanded.groupby(["publish_date", "category"]).size().reset_index(name="article_count")
    df_pivot = df_grouped.pivot(index="publish_date", columns="category", values="article_count").fillna(0)

    fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
    df_pivot.plot(ax=ax, marker='o', linestyle='-')

    # Chart formatting
    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.legend(title="", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10,
              facecolor="#0E1117", edgecolor="#0E1117", labelcolor="white")
    ax.grid(True, linestyle="--", alpha=0.7, color="gray")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.tick_params(axis='x', which='both', bottom=False, colors='white')
    ax.tick_params(axis='y', which='both', left=False, colors='white')
    plt.xticks(rotation=45, ha="right")

    return fig

def get_date_range():
    """
    Retrieves the earliest and latest publication dates from the news database.
    
    Returns:
        tuple: A tuple containing the earliest and latest publication dates.
    """
    cnxn = get_db_connection()
    cursor = cnxn.cursor(dictionary=True)
    cursor.execute("SELECT MIN(published) AS earliest, MAX(published) AS latest FROM news")
    result = cursor.fetchone()
    cursor.close()
    cnxn.close()
    return result["earliest"], result["latest"]

def main():
    """
    Main function to run the Streamlit application.
    
    Provides two views:
        1. News Articles View: Displays a list of news articles with filtering options.
        2. Data Analysis View: Displays visualizations (bar chart, line chart, word cloud) based on filtered data.
    """
    st.set_page_config(page_title="Nyhetsdashboard", layout="wide")
    st.sidebar.title("📌 Navigering")
    page = st.sidebar.radio("Välj en vy:", ["📰 Nyhetsartiklar", "📎 Dataanalys"])

    earliest_date, latest_date = get_date_range()
    earliest_date, latest_date = earliest_date.date(), latest_date.date()

    if page == "📰 Nyhetsartiklar":
        st.title("📰 AI-Klassificerade Nyhetsartiklar")
        articles = fetch_articles()

        # Extract unique categories from articles
        unique_categories = sorted(set(cat for article in articles for cat in json.loads(article["topic"])))

        st.sidebar.subheader("⚙️ Filteralternativ")
        selected_category = st.sidebar.selectbox("📂 Filtrera efter kategori:", ["Alla"] + unique_categories)
        start_date = st.sidebar.date_input(f"📅 Från och med: (Äldsta: {earliest_date})", earliest_date)
        end_date = st.sidebar.date_input(f"📅 Till och med: (Nyaste: {latest_date})", latest_date)
        search_query = st.sidebar.text_input("🔍 Sök efter artiklar")
        sort_option = st.sidebar.radio("Sortera efter:", ["Nyast först", "Äldst först"])

        filtered_articles = articles

        # Filter by category if not "Alla"
        if selected_category != "Alla":
            filtered_articles = [row for row in filtered_articles if selected_category in json.loads(row["topic"])]

        # Ensure publication date is a datetime object
        for row in filtered_articles:
            if isinstance(row["published"], datetime.date) and not isinstance(row["published"], datetime.datetime):
                row["published"] = datetime.datetime.combine(row["published"], datetime.datetime.min.time())

        # Filter articles by selected date range
        filtered_articles = [row for row in filtered_articles if start_date <= row["published"].date() <= end_date]

        # Filter articles by search query in title or summary
        if search_query:
            filtered_articles = [
                row for row in filtered_articles 
                if search_query.lower() in row['title'].lower() or search_query.lower() in row['summary'].lower()
            ]

        # Sort articles by publication date
        if sort_option == "Nyast först":
            filtered_articles.sort(key=lambda x: x['published'], reverse=True)
        else:
            filtered_articles.sort(key=lambda x: x['published'])

        total_articles = len(filtered_articles)
        st.subheader(f"# Totalt antal artiklar efter filtrering: {total_articles}")

        # Display each filtered article
        for row in filtered_articles:
            with st.container():
                st.subheader(row['title'])
                st.write(row['summary'])
                st.write(f"🕒 Publicerad: {row['published']}")
                st.write(f"📂 Kategorier: {', '.join(json.loads(row['topic']))}")
                st.markdown(f"[🔗 Läs mer]({row['link']})")
                st.write("---")

    elif page == "📎 Dataanalys":
        st.title("📎 Dataanalys av nyhetsartiklar")
        st.sidebar.subheader("⚙️ Filteralternativ")
        start_date = st.sidebar.date_input(f"Från: (Äldsta: {earliest_date})", earliest_date)
        end_date = st.sidebar.date_input(f"Till: (Nyaste: {latest_date})", latest_date)

        filtered_articles = [row for row in fetch_articles() if start_date <= row["published"].date() <= end_date]
        total_articles = len(filtered_articles)

        # Create two columns for visualizations
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader(f"📊 Antal artiklar per kategori ({total_articles} artiklar totalt)")
            bar_chart_fig = generate_bar_chart(start_date, end_date)
            if bar_chart_fig:
                st.pyplot(bar_chart_fig)
            else:
                st.write("Ingen data tillgänglig för valt datumintervall.")

            st.write("---")

            st.subheader("📈 Antal artiklar per kategori per dag")
            line_chart_fig = generate_line_chart(start_date, end_date)
            if line_chart_fig:
                st.pyplot(line_chart_fig)
            else:
                st.write("Ingen data tillgänglig för valt datumintervall.")

            st.write("---")

            st.subheader("☁️ Vanligaste orden i nyhetsartiklarna")
            wordcloud_fig = generate_wordcloud(start_date, end_date)
            if wordcloud_fig:
                st.pyplot(wordcloud_fig)
            else:
                st.write("Ingen text tillgänglig för att skapa en WordCloud.")

if __name__ == "__main__":
    main()
