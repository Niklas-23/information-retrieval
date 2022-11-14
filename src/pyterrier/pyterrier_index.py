import os
from typing import List

import pandas as pd
import pyterrier as pt

from arqmath_code.Entities.Post import Answer
from arqmath_code.topic_file_reader import Topic
from src.pyterrier.pyterrier_math_formula_coding import *
from src.pyterrier.config import ROOT_DIRECTORY

dict_field_names = ("docno", "text", "origtext", "parentno", "votes")


def get_pyterrier_answer_dict(documents: List[Answer]):
    for answer in documents:
        if answer.body is not None and answer.post_id is not None and answer.parent_id is not None and answer.votes is not None:
            indexed_body = translate_latex(answer.body)

            yield {'docno': answer.post_id,
                   'text': indexed_body,
                   'origtext': answer.body,
                   'parentno': answer.parent_id,
                   'votes': answer.votes
                   }


def get_pyterrier_query_dict(queries: List[Topic]):
    query_dict = []
    for topic in queries:
        query_dict.append({'qid': topic.topic_id, 'query': translate_latex(topic.question)})
    queries_data_frame = pd.DataFrame(query_dict)
    return queries_data_frame


def create_pyterrier_index(documents: List[Answer], index_name: str = "arqmath_indexV1"):
    index_path = f"{ROOT_DIRECTORY}/index/{index_name}"
    print(index_path)
    if not pt.started():
        pt.init()
    if not os.path.exists(index_path + "/data.properties"):
        indexer = pt.index.IterDictIndexer(index_path)
        index_reference = indexer.index(get_pyterrier_answer_dict(documents))
        pass
    else:
        index_reference = pt.IndexRef.of(index_path + "/data.properties")
        pass

    index = pt.IndexFactory.of(index_reference)
    return index
