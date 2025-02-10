"""
MLModelMLC_3.py

This script trains a multi-label text classification model using data from Book1.csv.
It:
  - Loads and preprocesses the data
  - Trains an SVC-based OneVsRest model with GridSearchCV
  - Prints out the best model and accuracy
  - Exposes key variables for import into other scripts:
       categories, x_train, vectorizer, best_clf_pipeline

"""

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

# Suppress warnings for clarity
if not sys.warnoptions:
    warnings.simplefilter("ignore")

# Load the dataset
DATA_PATH = "C:\\workspace\\ML\\ML-grupp6\\Gruppuppgift\\Book1.csv"
data_raw = pd.read_csv(DATA_PATH)
data_raw = data_raw.sample(frac=1)  # Shuffle data

# Extract categories (excluding 'Id' and 'Heading')
categories = list(data_raw.columns[2:])

# Preprocessing: clean text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    return text

data_raw['Heading'] = data_raw['Heading'].apply(preprocess_text)

# Remove stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('swedish'))
data_raw['Heading'] = data_raw['Heading'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

# Apply stemming
stemmer = SnowballStemmer("swedish")
data_raw['Heading'] = data_raw['Heading'].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split()]))

# Split the dataset
train, test = train_test_split(data_raw, random_state=42, test_size=0.30, shuffle=True)
x_train_text = train['Heading']
x_test_text = test['Heading']

y_train = train.drop(labels=['Id', 'Heading'], axis=1)
y_test = test.drop(labels=['Id', 'Heading'], axis=1)

# Vectorization
vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2')
vectorizer.fit(x_train_text)

x_train = vectorizer.transform(x_train_text)
x_test = vectorizer.transform(x_test_text)

# Define SVC model with GridSearchCV
param_grid = {
    'clf__estimator__C': [0.1, 1, 10, 100],
    'clf__estimator__kernel': ['linear', 'rbf'],
    'clf__estimator__gamma': [0.0001, 0.001, 0.01, 0.1]
}
svc_pipeline = Pipeline([
    ('clf', OneVsRestClassifier(SVC(probability=True)))
])

grid = GridSearchCV(svc_pipeline, param_grid, cv=10, scoring='accuracy', n_jobs=-1)
grid.fit(x_train, y_train)

# Output best parameters and accuracy
print("Best parameters:", grid.best_params_)
print("Best cross-validation score:", grid.best_score_)

best_clf_pipeline = grid.best_estimator_
best_clf_pipeline.fit(x_train, y_train)

# Predict on test data
y_pred = best_clf_pipeline.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print("Test Accuracy:", accuracy)

# Expose key objects for other scripts
categories = categories
x_train = x_train
vectorizer = vectorizer
best_clf_pipeline = best_clf_pipeline
