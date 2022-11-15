from itertools import groupby
from typing import Tuple, List, Union

from arqmath_code.Entities.Post import Answer, Question
from arqmath_code.topic_file_reader import Topic
from src.base.post_processor import PostProcessor


class TopKFilter(PostProcessor):

    def __init__(self, k=1000):
        self.k = k
        pass

    def forward(self, queries: List[Topic], ranking: List[Tuple[Topic, Union[Question, Answer], float]]) -> List[
        Tuple[Topic, Union[Question, Answer], float]]:
        result = []
        for key, group in groupby(ranking, key=lambda tuple: tuple[0].topic_id):
            group = list(group)
            sorted_group = sorted(group, key=lambda tuple: tuple[2], reverse=True)[:self.k]
            result.extend(sorted_group)
        return result
