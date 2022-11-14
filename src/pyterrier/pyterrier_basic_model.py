from typing import Tuple, Union, List

from pandas import DataFrame

from arqmath_code.Entities.Post import Answer, Question
from arqmath_code.topic_file_reader import Topic
from src.base.model import Model
from src.pyterrier.pyterrier_index import create_pyterrier_index, get_pyterrier_query_dict
import pyterrier as pt


class BasicPyTerrierModel(Model):

    def __init__(self, pyterrier_model: str = "TF_IDF"):
        self.pyterrier_index = None
        self.pyterrier_model = pyterrier_model
        pass

    def forward(self, queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[
        Tuple[Topic, Union[Question, Answer], float]]:

        if type(documents) is List[Question]:
            raise Exception("Question can't be indexed using the basic PyTerrier model")

        if not pt.started():
            pt.init()

        self.pyterrier_index = create_pyterrier_index(documents=documents, index_name="pyterrier_answer_index_task1_v1")

        batch_retrieve = pt.BatchRetrieve(self.pyterrier_index, wmodel=self.pyterrier_model)
        queries_data_frame = get_pyterrier_query_dict(queries)
        ranking: DataFrame = batch_retrieve.transform(queries_data_frame)
        documents_to_include = set([answer.post_id for answer in documents])
        result = []
        for index, row in ranking.iterrows():
            post_id = int(row["docno"])
            if post_id in documents_to_include:
                topic = next((topic for topic in queries if topic.topic_id == row["qid"]), None)
                answer = next((answer for answer in documents if answer.post_id == post_id), None)
                result.append((topic, answer, row["score"]))

        return result
