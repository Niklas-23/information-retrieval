from typing import Tuple, Union, List

from pandas import DataFrame

from arqmath_code.Entities.Post import Answer, Question
from arqmath_code.topic_file_reader import Topic
from src.base.model import Model
from src.pyterrier.pyterrier_index import create_pyterrier_index, get_pyterrier_query_dict
import pyterrier as pt


class BasicPyTerrierModel(Model):

    def __init__(self, pyterrier_model: str = "TF_IDF", pyterrier_index_name: str = "pyterrier_answer_index_task1_v1"):
        self.pyterrier_index = None
        self.pyterrier_model = pyterrier_model
        self.pyterrier_index_name = pyterrier_index_name
        pass

    def forward(self, queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[
        Tuple[Topic, Union[Question, Answer], float]]:

        if type(documents) is List[Question]:
            raise Exception("Question can't be indexed using the basic PyTerrier model")

        if not pt.started():
            pt.init()

        self.pyterrier_index = create_pyterrier_index(documents=documents, index_name=self.pyterrier_index_name)

        batch_retrieve = pt.BatchRetrieve(self.pyterrier_index, wmodel=self.pyterrier_model)
        queries_data_frame = get_pyterrier_query_dict(queries)
        ranking: DataFrame = batch_retrieve.transform(queries_data_frame)

        documents_to_include = set([answer.post_id for answer in documents])
        documents_dict = {answer.post_id: answer for answer in documents}
        queries_dict = {topic.topic_id: topic for topic in queries}

        result = []
        for index, row in ranking.iterrows():
            if int(row["docno"]) in documents_to_include:
                topic = queries_dict[row["qid"]]
                answer = documents_dict[int(row["docno"])]
                result.append((topic, answer, row["score"]))

        return result
