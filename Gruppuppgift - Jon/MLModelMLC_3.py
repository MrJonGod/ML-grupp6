"""
MLModelMLC_3.py

This script trains a multi-label text classification model using data from Book1_2.csv.
It:
  - Loads and preprocesses the data
  - Trains an SVC-based OneVsRest model with GridSearchCV (if not cached)
  - Caches both the fitted vectorizer and the trained model to save time on subsequent runs
  - Prints out the best model parameters and test accuracy
  - Exposes key variables for import into other scripts:
       categories, x_train, vectorizer, best_clf_pipeline
"""

import os
import joblib
import re
import sys
import warnings
import nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from tokenizer_utils import custom_tokenizer

# Suppress warnings for clarity
if not sys.warnoptions:
    warnings.simplefilter("ignore")

# Ensure that stopwords are downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Initialize Swedish stopwords and stemmer
stop_words = set(stopwords.words('swedish'))
stemmer = SnowballStemmer("swedish")

# Load the dataset
DATA_PATH = "C:\\workspace\\ML\\ML-grupp6\\Gruppuppgift\\Book1_2.csv"
data_raw = pd.read_csv(DATA_PATH)
data_raw = data_raw.sample(frac=1)  # Shuffle the data

# Extract categories (excluding 'Id' and 'Heading')
categories = list(data_raw.columns[2:])

# Replace NaN with 0
data_raw.fillna(0, inplace=True)

# Split the dataset into training and testing sets
train, test = train_test_split(data_raw, random_state=42, test_size=0.30, shuffle=True)
x_train_text = train['Heading']
x_test_text = test['Heading']

y_train = train.drop(labels=['Id', 'Heading'], axis=1)
y_test = test.drop(labels=['Id', 'Heading'], axis=1)

# Define file paths for caching the vectorizer and model
VECTORIZER_PATH = "vectorizer.pkl"  # Path to save/load the fitted vectorizer
MODEL_PATH = "best_clf_pipeline.pkl"  # Path to save/load the trained model

# Caching for the vectorizer:
# If the cached vectorizer exists, load it; otherwise, create, fit, and save it.
if os.path.exists(VECTORIZER_PATH):
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Vectorizer loaded from disk.")
else:
    vectorizer = TfidfVectorizer(
        tokenizer=custom_tokenizer,  # Custom tokenizer for preprocessing
        preprocessor=None,           # Disable built-in preprocessing as it's handled in the tokenizer
        lowercase=False,             # Already lowercased in the tokenizer
        analyzer='word',
        ngram_range=(1, 3),
        norm='l2'
    )
    vectorizer.fit(x_train_text)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print("Vectorizer fitted and saved to disk.")

# Transform training and testing texts using the (cached or newly fitted) vectorizer
x_train = vectorizer.transform(x_train_text)
x_test = vectorizer.transform(x_test_text)

# Define the SVC model inside a pipeline with OneVsRestClassifier
svc_pipeline = Pipeline([
    ('clf', OneVsRestClassifier(SVC(probability=True)))
])

# Parameter grid for GridSearchCV
param_grid = {
    'clf__estimator__C': [0.1, 1, 10, 100],
    'clf__estimator__kernel': ['linear', 'rbf'],
    'clf__estimator__gamma': [0.0001, 0.001, 0.01, 0.1]
}

# Caching for the model:
# If the cached model exists, load it; otherwise, perform GridSearchCV and save the trained model.
if os.path.exists(MODEL_PATH):
    best_clf_pipeline = joblib.load(MODEL_PATH)
    print("Model pipeline loaded from disk.")
else:
    grid = GridSearchCV(svc_pipeline, param_grid, cv=10, scoring='accuracy', n_jobs=-1)
    grid.fit(x_train, y_train)
    best_clf_pipeline = grid.best_estimator_
    joblib.dump(best_clf_pipeline, MODEL_PATH)
    print("Model trained and saved to disk.")
    print("Best parameters:", grid.best_params_)
    print("Best cross-validation score:", grid.best_score_)

# Evaluate the model on test data
y_pred = best_clf_pipeline.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print("Test Accuracy:", accuracy)

# Expose key objects for other scripts
# These variables can be imported by other modules
categories = categories
x_train = x_train
vectorizer = vectorizer
best_clf_pipeline = best_clf_pipeline

"""
Best parameters: {'clf__estimator__C': 10, 'clf__estimator__gamma': 0.0001, 'clf__estimator__kernel': 'linear'}
Best cross-validation score: 0.2623595505617977
Test Accuracy: 0.39528795811518325
"""
