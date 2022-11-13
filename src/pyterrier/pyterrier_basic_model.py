from typing import Tuple, Union, List

from arqmath_code.Entities.Post import Answer, Question
from arqmath_code.topic_file_reader import Topic
from src.base.model import Model
from src.pyterrier.pyterrier_index import create_pyterrier_index
import pyterrier as pt


class BasicPyTerrierModel(Model):

    def __init__(self, pyterrier_model: str = "TF_IDF"):
        self.pyterrier_index = None
        self.pyterrier_model = pyterrier_model
        pass

    def forward(self, queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[
        Tuple[Topic, Union[Question, Answer], float]]:
        if type(documents) is List[Question]:
            raise Exception("Question can't be index using the basic PyTerrier model")
        self.pyterrier_index = create_pyterrier_index(documents=documents, index_name="pyterrier_answer_index_task1_v1")
        batch_retrieve = pt.BatchRetrieve(self.pyterrier_index, wmodel=self.pyterrier_model)
        ranking = batch_retrieve.search(queries)
        documents_to_include = set([answer.post_id for answer in documents])
        ranking = ranking[ranking.docno in documents_to_include]
        return ranking
