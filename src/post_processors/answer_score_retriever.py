from typing import List, Tuple, Union

from arqmath_code.Entities.Post import Question, Answer
from arqmath_code.topic_file_reader import Topic
from src.base.post_processor import PostProcessor


class AnswerScoreRetriever(PostProcessor):

    def forward(self, queries: List[Topic], ranking: List[Tuple[Topic, Union[Question, Answer], float]]) -> List[
        Tuple[Topic, Union[Question, Answer], float]]:
        ranking = filter(lambda t: t[1].answers is not None, ranking)
        return [
            (topic, question.accepted_answer_id, score)
            if question.accepted_answer_id is not None
            else (topic, question.answers[0].post_id, score)
            for topic, question, score in ranking
        ]
