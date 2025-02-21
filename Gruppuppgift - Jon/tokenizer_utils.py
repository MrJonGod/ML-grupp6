import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# Ensure stopwords are available
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

stop_words = set(stopwords.words('swedish'))
stemmer = SnowballStemmer("swedish")

def custom_tokenizer(text):
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    tokens = text.split()
    tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]
    return tokens
