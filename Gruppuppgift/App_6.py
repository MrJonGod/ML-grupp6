"""
App_6.py
News Dashboard Application

This Streamlit application connects to a MySQL database to fetch, filter, and display AI-classified news articles.
It provides two main views:
    1. News Articles View: Lists news articles with filtering options.
    2. Data Analysis View: Displays visualizations including a bar chart, line chart, and word cloud.
"""

# Standard library imports
import json
import datetime
from contextlib import contextmanager

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

@contextmanager
def get_db_cursor(dictionary=True):
    """
    Context manager that yields a MySQL database cursor.
    
    Ensures that the connection and cursor are properly closed.
    """
    cnxn = mysql.connector.connect(**DB_CONFIG)
    cursor = cnxn.cursor(dictionary=dictionary)
    try:
        yield cursor
    finally:
        cursor.close()
        cnxn.close()

@st.cache_data
def get_date_range():
    """
    Retrieves the earliest and latest publication dates from the news database.
    
    Returns:
        tuple: A tuple containing the earliest and latest publication dates.
    """
    with get_db_cursor() as cursor:
        cursor.execute("SELECT MIN(published) AS earliest, MAX(published) AS latest FROM news")
        result = cursor.fetchone()
    return result["earliest"], result["latest"]

@st.cache_data
def fetch_articles_filtered(start_date, end_date, category, search_query, sort_order):
    """
    Retrieves filtered news articles based on date range, category, and search query directly from the database.
    The end_date is adjusted to include the entire day by adding one day and using a half-open interval.
    
    Args:
        start_date (date): The start date for filtering.
        end_date (date): The end date for filtering.
        category (str): Category filter; if "Alla", no filtering is applied.
        search_query (str): Text to search for in title or summary.
        sort_order (str): "Nyast först" or "Äldst först" for sorting.
    
    Returns:
        list: A list of dictionaries representing the filtered news articles.
    """
    # Adjust end_date to include the entire day
    end_date_exclusive = end_date + datetime.timedelta(days=1)
    query = "SELECT * FROM news WHERE published >= %s AND published < %s"
    params = [start_date, end_date_exclusive]
    
    # Apply category filter if not "Alla"
    if category and category != "Alla":
        query += " AND JSON_CONTAINS(topic, %s)"
        params.append(f'"{category}"')
    
    # Apply search filter if provided
    if search_query:
        query += " AND (LOWER(title) LIKE %s OR LOWER(summary) LIKE %s)"
        like_query = f"%{search_query.lower()}%"
        params.extend([like_query, like_query])
    
    # Apply sorting based on user selection
    if sort_order == "Nyast först":
        query += " ORDER BY published DESC"
    else:
        query += " ORDER BY published ASC"
    
    with get_db_cursor() as cursor:
        cursor.execute(query, tuple(params))
        articles = cursor.fetchall()
    return articles

def fetch_category_counts(start_date, end_date):
    """
    Retrieves the count of articles per category within the specified date range.
    
    Args:
        start_date (date): The start date for filtering.
        end_date (date): The end date for filtering.
    
    Returns:
        dict: A dictionary with category names as keys and counts as values.
    """
    end_date_exclusive = end_date + datetime.timedelta(days=1)
    with get_db_cursor() as cursor:
        query = "SELECT topic FROM news WHERE published >= %s AND published < %s"
        cursor.execute(query, (start_date, end_date_exclusive))
        topics = cursor.fetchall()
    
    category_count = {}
    for row in topics:
        categories = json.loads(row["topic"])
        for category in categories:
            category_count[category] = category_count.get(category, 0) + 1
    return category_count

def generate_wordcloud(start_date, end_date):
    """
    Generates a WordCloud visualization based on article summaries within the specified date range.
    
    Args:
        start_date (date): The start date for filtering.
        end_date (date): The end date for filtering.
    
    Returns:
        matplotlib.figure.Figure or None: The WordCloud figure if text exists; otherwise, None.
    """
    end_date_exclusive = end_date + datetime.timedelta(days=1)
    with get_db_cursor() as cursor:
        query = "SELECT summary FROM news WHERE published >= %s AND published < %s"
        cursor.execute(query, (start_date, end_date_exclusive))
        summaries = cursor.fetchall()
    
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
        start_date (date): The start date for filtering.
        end_date (date): The end date for filtering.
    
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
        start_date (date): The start date for filtering.
        end_date (date): The end date for filtering.
    
    Returns:
        matplotlib.figure.Figure or None: The line chart figure if data is available; otherwise, None.
    """
    end_date_exclusive = end_date + datetime.timedelta(days=1)
    with get_db_cursor() as cursor:
        query = "SELECT DATE(published) AS publish_date, topic FROM news WHERE published >= %s AND published < %s"
        cursor.execute(query, (start_date, end_date_exclusive))
        data = cursor.fetchall()
    
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

def main():
    """
    Main function to run the Streamlit application.
    
    Provides two views:
        1. News Articles View: Displays a list of news articles with filtering options.
        2. Data Analysis View: Displays visualizations based on filtered data.
    """
    st.set_page_config(page_title="Nyhetsdashboard", layout="wide")
    st.sidebar.title("📌 Navigering")
    page = st.sidebar.radio("Välj en vy:", ["📰 Nyhetsartiklar", "📎 Dataanalys"])

    earliest_date, latest_date = get_date_range()
    earliest_date, latest_date = earliest_date.date(), latest_date.date()

    if page == "📰 Nyhetsartiklar":
        st.title("📰 AI-Klassificerade Nyhetsartiklar")
        
        # Fetch all articles in the full date range to extract unique categories
        all_articles = fetch_articles_filtered(earliest_date, latest_date, "Alla", "", "Nyast först")
        unique_categories = sorted(set(cat for article in all_articles for cat in json.loads(article["topic"])))
        
        st.sidebar.subheader("⚙️ Filteralternativ")
        selected_category = st.sidebar.selectbox("Filtrera efter kategori:", ["Alla"] + unique_categories)
        start_date = st.sidebar.date_input(f"Från: (Äldsta: {earliest_date})", earliest_date)
        end_date = st.sidebar.date_input(f"Till: (Nyaste: {latest_date})", latest_date)
        search_query = st.sidebar.text_input("Sök efter artiklar")
        sort_option = st.sidebar.radio("Sortera efter:", ["Nyast först", "Äldst först"])

        articles = fetch_articles_filtered(start_date, end_date, selected_category, search_query, sort_option)
        total_articles = len(articles)
        st.subheader(f"# Totalt antal artiklar efter filtrering: {total_articles}")

        for row in articles:
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

        articles = fetch_articles_filtered(start_date, end_date, "Alla", "", "Nyast först")
        total_articles = len(articles)

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

            st.subheader("☁️ Vanligaste orden i nyhetsartiklar")
            wordcloud_fig = generate_wordcloud(start_date, end_date)
            if wordcloud_fig:
                st.pyplot(wordcloud_fig)
            else:
                st.write("Ingen text tillgänglig för att skapa en WordCloud.")

if __name__ == "__main__":
    main()
