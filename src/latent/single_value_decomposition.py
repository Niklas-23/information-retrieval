from typing import List, Union, Tuple

import numpy as np
from pandas import DataFrame
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from arqmath_code.Entities.Post import Question, Answer
from arqmath_code.topic_file_reader import Topic
from src.base.model import Model


class SingleValueDecompositionModel(Model):

    def __init__(self, svd_n_components=200, svd_random_state=2, vectorizer_max_df=0.90,
                 vectorizer_min_df=2, save_embeddings=False):
        self.svd_n_components = svd_n_components
        self.svd_random_state = svd_random_state
        self.vectorizer_max_df = vectorizer_max_df
        self.vectorizer_min_df = vectorizer_min_df
        self.save_embeddings = save_embeddings
        pass

    def forward(self, queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[
        Tuple[Topic, Union[Question, Answer], float]]:

        if type(documents) is List[Question]:
            raise Exception("Question are not allowed for this model")

        document_dataframe: DataFrame = DataFrame([document.body for document in documents], columns=["text"])
        count_vectorizer = CountVectorizer(max_df=self.vectorizer_max_df, min_df=self.vectorizer_min_df, lowercase=True)
        document_term_matrix = count_vectorizer.fit_transform(document_dataframe["text"])
        print("Finished count vectorizer")

        svd = TruncatedSVD(n_components=self.svd_n_components, random_state=self.svd_random_state)
        document_topics = svd.fit_transform(document_term_matrix)
        print("Finished SVD embedding")

        query_dataframe: DataFrame = DataFrame([topic.question for topic in queries], columns=["text"])
        query_term_matrix = count_vectorizer.transform(query_dataframe["text"])

        query_topics = svd.transform(query_term_matrix)
        cos_sims: np.ndarray = cosine_similarity(query_topics, document_topics)

        if self.save_embeddings:
            np.save("svd_embedding_answers", document_topics)
            np.save("svd_topics_embedding", query_topics)

        result = []
        for i, query in enumerate(queries):
            per_query = list(zip(range(cos_sims.shape[1]), cos_sims[i,]))
            for j in per_query:
                result.append((query, documents[j[0]], j[1]))

        return result
