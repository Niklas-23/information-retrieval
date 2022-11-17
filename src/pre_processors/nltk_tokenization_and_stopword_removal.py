from typing import Union, List

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

from arqmath_code.Entities.Post import Question, Answer
from arqmath_code.topic_file_reader import Topic
from src.base.pre_processing import PreProcessor
from src.base.query_pre_processor import QueryPreProcessor

nltk.download('stopwords')
nltk.download('punkt')
stop_word_set = set(stopwords.words('english'))


def tokenize_text(text: str) -> str:
    text_tokens = word_tokenize(text.lower())
    tokens_without_sw = [word for word in text_tokens if not word in stop_word_set]
    filtered_sentence = (" ").join(tokens_without_sw)
    return filtered_sentence


class NLTKTokenizationAndStopwordRemoval(PreProcessor):

    def forward(self, queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[Union[Question, Answer]]:
        for document in documents:
            document.body = tokenize_text(document.body)
            if isinstance(document, Question):
                document.title = tokenize_text(document.title)
        return documents


class NLTKTokenizationAndStopwordRemovalForQueries(QueryPreProcessor):

    def forward(self, queries: List[Topic]) -> List[Topic]:
        for topic in queries:
            topic.title = tokenize_text(topic.title)
            topic.question = tokenize_text(topic.question)
        return queries
