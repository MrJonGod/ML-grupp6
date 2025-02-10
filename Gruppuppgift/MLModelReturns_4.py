"""
MLModelReturns_4.py

This script automatically classifies news articles fetched from RSS feeds using a pre-trained machine learning model.
It:
  - Imports 'MyTheFinalList' from FullRSSList_1_2.py
  - Loads the trained model (best_clf_pipeline) and supporting objects (categories, vectorizer) from MLModelMLC_3.py
  - Preprocesses the RSS article data for classification
  - Uses the model to predict categories, ensuring each article receives at least one category
  - Validates and structures the predictions in a dictionary format
"""

import json
import numpy as np
from FullRSSList_1_2 import MyTheFinalList
from MLModelMLC_3 import categories, vectorizer, best_clf_pipeline

# Define the classification probability threshold
THRESHOLD = 0.3

def preprocess_text(article_list):
    """
    Combines article title and summary into a single text representation for classification.
    """
    return [f"{article[0]} {article[1]}" for article in article_list if article[0].strip() and article[1].strip()]

def classify_articles(articles_texts):
    """
    Transforms preprocessed article texts into numerical features and classifies them using the trained model.
    Ensures that each article gets at least one category.
    """
    transformed_texts = vectorizer.transform(articles_texts)
    predictions = best_clf_pipeline.predict_proba(transformed_texts)
    
    classified_results = []
    for prob_vector in predictions:
        # Identify categories that meet the threshold
        predicted_categories = [categories[i] for i, prob in enumerate(prob_vector) if prob >= THRESHOLD]
        
        # If no category meets the threshold, select the one with the highest probability
        if not predicted_categories:
            best_category = categories[np.argmax(prob_vector)]
            predicted_categories = [best_category]
        
        classified_results.append(predicted_categories)
    
    return classified_results

def create_final_dict(article_list, predicted_labels):
    """
    Combines original article data with predicted categories to form a structured dictionary.
    """
    return [
        {
            "title": article[0],
            "summary": article[1],
            "link": article[2],
            "published": article[3],
            "categories": predicted_labels[i]
        }
        for i, article in enumerate(article_list)
    ]

def validate_data(final_list):
    """
    Validates the generated dictionary structure.
    """
    return [item for item in final_list if isinstance(item, dict)]

def main():
    """
    Main execution function to preprocess articles, classify them, structure results, and validate.
    """
    global validDict
    articles_texts = preprocess_text(MyTheFinalList)
    predicted_labels = classify_articles(articles_texts)
    final_data = create_final_dict(MyTheFinalList, predicted_labels)
    validDict = validate_data(final_data)
    print(json.dumps(validDict, indent=4, ensure_ascii=False))
    return validDict

if __name__ == "__main__":
    validDict = main()
