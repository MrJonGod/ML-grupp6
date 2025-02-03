"""
=================================================
  MACHINE LEARNING TECHNIQUES INLAMNING 2
=================================================
In this script:
1. We load data from Book1.csv.
2. We clean, tokenize, remove stopwords, and (optionally) stem the text in the 'Heading' column.
3. We split into train/test sets and convert the text to TF-IDF features.

At the end, we have:
    x_train, x_test : TF-IDF feature matrices
    y_train, y_test : DataFrames with target labels

Your tasks (outlined below) focus on building and evaluating
machine learning models to classify these text entries.
"""

import re
import sys
import warnings
import nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Adjust this path to where your NLTK data is located
nltk.data.path.append('/usr/local/share/nltk_data')

# Suppress all warning messages
if not sys.warnoptions:
    warnings.simplefilter("ignore")

# 1. Load the data
data_path = "/Users/Hanne/Portofolio/Text-Classification/Book1.csv"
data_raw = pd.read_csv(data_path)

# 2. Shuffle the data
data_raw = data_raw.sample(frac=1)

# 3. Identify category columns
categories = list(data_raw.columns.values)
categories = categories[2:]  # Adjust if your CSV structure changes

# 4. Basic cleaning on the "Heading" column
data_raw['Heading'] = (
    data_raw['Heading']
    .str.lower()
    .str.replace('[^\w\s]', '', regex=True)     # remove punctuation
    .str.replace('\d+', '', regex=True)         # remove digits
    .str.replace('<.*?>', '', regex=True)       # remove HTML tags
)

# 5. Download stopwords and define your stop-word removal function
nltk.download('stopwords')
stop_words = set(stopwords.words('swedish'))

def removeStopWords(sentence):
    return " ".join(
        [word for word in nltk.word_tokenize(sentence) 
         if word not in stop_words]
    )

data_raw['Heading'] = data_raw['Heading'].apply(removeStopWords)

# 6. (Optional) Stemming
stemmer = SnowballStemmer("swedish")

def stemming(sentence):
    stemSentence = ""
    for word in sentence.split():
        stemSentence += stemmer.stem(word) + " "
    return stemSentence.strip()

# If you want to apply stemming, uncomment:
# data_raw['Heading'] = data_raw['Heading'].apply(stemming)

# 7. Split the data
train, test = train_test_split(data_raw, random_state=42, test_size=0.30, shuffle=True)

train_text = train['Heading']
test_text = test['Heading']

# 8. Vectorize using TF-IDF
vectorizer = TfidfVectorizer(strip_accents='unicode', 
                             analyzer='word', 
                             ngram_range=(1,3), 
                             norm='l2')
vectorizer.fit(train_text)

x_train = vectorizer.transform(train_text)
y_train = train.drop(labels=['Id', 'Heading'], axis=1)

x_test = vectorizer.transform(test_text)
y_test = test.drop(labels=['Id', 'Heading'], axis=1)


#####################################################
#  PART 1: CHOOSE A CLASSIFIER
#####################################################
"""
In this part, you will:
1. Import or define the classification algorithm(s) you want to try.
2. Examples: LogisticRegression, MultinomialNB (Naive Bayes), SVC, RandomForestClassifier, etc.
3. You can handle multi-label classification if the dataset requires it
   (e.g., OneVsRestClassifier, MultiOutputClassifier, etc.).

Code outline might look like:

from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()
# or
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()

Feel free to experiment with multiple classifiers.
"""

# Your CODE HERE:
# -------------------------------------------------
# e.g.,
# from sklearn.linear_model import LogisticRegression
# clf = LogisticRegression()
# -------------------------------------------------


#####################################################
#  PART 2: TRAIN YOUR MODEL
#####################################################
"""
Now, train (fit) your chosen classifier on (x_train, y_train).

Example:

clf.fit(x_train, y_train)

After this step, your model will be "trained" on the training data.
"""

# Your CODE HERE:
# -------------------------------------------------
# e.g.,
# clf.fit(x_train, y_train)
# -------------------------------------------------


#####################################################
#  PART 3: MAKE PREDICTIONS
#####################################################
"""
Use your trained model to predict labels on the test set (x_test).
Store the predictions in a variable, e.g. y_pred.

Example:

y_pred = clf.predict(x_test)
"""

# Your CODE HERE:
# -------------------------------------------------
# y_pred = clf.predict(x_test)
# -------------------------------------------------


#####################################################
#  PART 4: EVALUATE PERFORMANCE
#####################################################
"""
Now evaluate how well your model performs using metrics such as:
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix, if relevant.

Example with accuracy:
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

You can also explore other metrics from sklearn.metrics (e.g., classification_report).
"""

# Your CODE HERE:
# -------------------------------------------------
# from sklearn.metrics import accuracy_score
# accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)
#
# # Possibly more metrics:
# from sklearn.metrics import classification_report
# print(classification_report(y_test, y_pred))
# -------------------------------------------------


#####################################################
#  PART 5: TUNE HYPERPARAMETERS
#####################################################
"""
Use GridSearchCV or RandomizedSearchCV to find the best parameters
for your chosen classifier.

Example:

from sklearn.model_selection import GridSearchCV

param_grid = {'C': [0.1, 1, 10], 'penalty': ['l1', 'l2']}
clf_base = LogisticRegression(solver='liblinear') 
# (solver='liblinear' helps with small data or L1 penalty)

grid = GridSearchCV(clf_base, param_grid, cv=5, scoring='accuracy')
grid.fit(x_train, y_train)

print("Best params: ", grid.best_params_)
print("Best score: ", grid.best_score_)

Then retrain your final model using these best params:

best_clf = grid.best_estimator_
best_clf.fit(x_train, y_train)

Proceed to evaluate as in PART 4.
"""

# Your CODE HERE:
# -------------------------------------------------
# param_grid = {...}
# from sklearn.model_selection import GridSearchCV
# grid = GridSearchCV(..., param_grid, ...)
# grid.fit(x_train, y_train)
# print(grid.best_params_, grid.best_score_)
# -------------------------------------------------


#####################################################
#  PART 6: COMPARE
#####################################################
"""
If you try multiple classifiers (LogisticRegression, SVC, Random Forest, etc.), 
you can compare their performance. Keep track of the metrics and see which 
classifier + hyperparameter combo works best for this dataset.
"""

# Your CODE HERE:
# -------------------------------------------------
# e.g.,
# classifiers = [LogisticRegression(...), SVC(...), RandomForestClassifier(...)]
# for model in classifiers:
#     ...
#     Evaluate
#     ...
# -------------------------------------------------

