from typing import List, Union, Tuple

from sentence_transformers import CrossEncoder

from arqmath_code.Entities.Post import Answer, Question
from arqmath_code.topic_file_reader import Topic
from src.base.post_processor import PostProcessor


class SBertCrossEncoder(PostProcessor):

    def __init__(self, model_id):
        self.cross_encoder = CrossEncoder(model_id)

    def forward(self, queries: List[Topic], ranking: List[Tuple[Topic, Union[Question, Answer], float]]) -> List[
        Tuple[Topic, Union[Question, Answer], float]]:
        cross_encoder_in = [[topic.question, answer.body] for topic, answer, _ in ranking]
        scores = self.cross_encoder.predict(cross_encoder_in, show_progress_bar=True)
        print(scores)
        res_ranking = [(ranking[i][0], ranking[i][1], scores[i]) for i in range(len(ranking))]
        return res_ranking
