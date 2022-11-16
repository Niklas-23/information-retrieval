from typing import List, Union, Tuple

import numpy as np
from pandas import DataFrame
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from arqmath_code.Entities.Post import Question, Answer
from arqmath_code.topic_file_reader import Topic
from src.base.model import Model


class LatentDirichletAllocationModel(Model):

    def __init__(self, lda_n_components=200, lda_random_state=2, lda_n_jobs=-1, vectorizer_max_df=0.90,
                 vectorizer_min_df=2):
        self.lda_n_components = lda_n_components
        self.lda_random_state = lda_random_state
        self.lda_n_jobs = lda_n_jobs  # -1 to use all available cpu cores
        self.vectorizer_max_df = vectorizer_max_df
        self.vectorizer_min_df = vectorizer_min_df
        pass

    def forward(self, queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[
        Tuple[Topic, Union[Question, Answer], float]]:

        if type(documents) is List[Question]:
            raise Exception("Question are not allowed for this model")

        document_dataframe: DataFrame = DataFrame([document.body for document in documents], columns=["text"])
        count_vectorizer = CountVectorizer(max_df=self.vectorizer_max_df, min_df=self.vectorizer_min_df, lowercase=True)
        document_term_matrix = count_vectorizer.fit_transform(document_dataframe["text"])
        print("Finished count vectorizer")

        lda = LatentDirichletAllocation(n_components=self.lda_n_components, random_state=self.lda_random_state,
                                        n_jobs=self.lda_n_jobs)
        document_topics = lda.fit_transform(document_term_matrix)
        print("Finished LDA embedding")

        query_dataframe: DataFrame = DataFrame([topic.question for topic in queries], columns=["text"])
        query_term_matrix = count_vectorizer.transform(query_dataframe["text"])

        query_topics = lda.transform(query_term_matrix)
        cos_sims: np.ndarray = cosine_similarity(query_topics, document_topics)

        result = []
        for i, query in enumerate(queries):
            per_query = list(zip(range(cos_sims.shape[1]), cos_sims[i,]))
            for j in per_query:
                result.append((query, documents[j[0]], j[1]))

        return result
