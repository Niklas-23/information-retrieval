from typing import Union, List

from bs4 import BeautifulSoup

from arqmath_code.Entities.Post import Question, Answer
from arqmath_code.topic_file_reader import Topic
from src.base.pre_processing import PreProcessor
from src.base.query_pre_processor import QueryPreProcessor


def remove_xml_tags(text: str) -> str:
    return BeautifulSoup(text, features="lxml").text


class RemoveXMLTagsFromDocumentBody(PreProcessor):

    def forward(self, queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[Union[Question, Answer]]:
        for document in documents:
            document.body = remove_xml_tags(document.body)
            if isinstance(document, Question):
                document.title = remove_xml_tags(document.title)
        return documents


class RemoveXMLTagsFromQueries(QueryPreProcessor):

    def forward(self, queries: List[Topic]) -> List[Topic]:
        for topic in queries:
            topic.title = remove_xml_tags(topic.title)
            topic.question = remove_xml_tags(topic.question)
        return queries
