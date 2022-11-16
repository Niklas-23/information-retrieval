import nltk
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
stop_word_set = set(stopwords.words('english'))


def tokenize_text(text: str) -> str:
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stop_word_set]
    filtered_sentence = (" ").join(tokens_without_sw)
    return filtered_sentence


def remove_xml_tags(text: str) -> str:
    return BeautifulSoup(text, features="lxml").text
