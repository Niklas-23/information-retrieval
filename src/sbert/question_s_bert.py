from numpy import ndarray
import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from torch import Tensor
from src.base.model import Model
from sentence_transformers.util import cos_sim
from typing import List, Union, Tuple, Dict
from arqmath_code.topic_file_reader import Topic
from arqmath_code.Entities.Post import Question, Answer
import os
import json


class QuestionSBERT(Model):

    def __init__(self, model_id: str):
        self.model = SentenceTransformer(model_id)
        self.path = '../arqmath_dataset/model_embeddings/'
        self.document_path = os.path.join(self.path, f"document_embeddings_{model_id}.npy")
        self.index_path = os.path.join(self.path, f"index_{model_id}.json")

    def _save_embeddings(self, embedding: Union[list[Tensor], ndarray, ndarray, Tensor],
                         document_index: Dict[int, Union[Question, Answer]]):
        np.save(self.document_path, embedding)
        index_to_save = {index: document.post_id for index, document in document_index.items()}
        with open(self.index_path, 'w+') as file:
            file.write(json.dumps(index_to_save))

    def _load_embeddings(self, documents: List[Union[Question, Answer]]) -> (
    ndarray, Dict[int, Union[Question, Answer]]):
        embeddings = np.load(self.document_path)
        id_to_object_index = {doc.post_id: doc for doc in documents}
        with open(self.index_path, 'r') as f:
            saved_index: Dict[int, int] = json.load(f)
        document_index = {int(index): id_to_object_index[doc_id] for index, doc_id in saved_index.items()}
        return embeddings, document_index

    def forward(self, queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[
        Tuple[Topic, Union[Question, Answer], float]]:
        if not os.path.isfile(self.document_path):
            document_title_embeddings = self.model.encode([document.title for document in documents])
            document_index = {documents.index(document): document for document in documents}
            self._save_embeddings(embedding=document_title_embeddings, document_index=document_index)

        else:
            print("read from cached embeddings at ", self.document_path)
            document_title_embeddings, document_index = self._load_embeddings(documents=documents)

        query_title_embeddings = self.model.encode([query.title for query in queries])
        scores: torch.Tensor = cos_sim(query_title_embeddings, document_title_embeddings)  # r[i] -> row of query sims
        res: np.ndarray = np.array(
            [list(zip(
                [queries[i] for _ in range(scores[i].size()[0])],
                [document_index[idx] for idx in range(scores[i].size()[0])],
                scores[i].numpy()
            )) for i in range(scores.size()[0])]
        )
        res = res.reshape(res.shape[0] * res.shape[1], res.shape[2])
        return list(map(lambda arr: tuple(arr), res))
