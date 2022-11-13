import os
from typing import List

import pyterrier as pt
from pyterrier.index import IterDictIndexer, IndexRef

from arqmath_code.Entities.Post import Answer
from arqmath_code.post_reader_record import DataReaderRecord
from src.pyterrier.pyterrier_math_formula_coding import *
from src.pyterrier.config import ROOT_DIRECTORY

dict_field_names = ("docno", "text", "origtext", "parentno", "votes")

def get_arqmath_answers_as_iterable(data_reader: DataReaderRecord):
    for answer in data_reader.get_all_answer_posts():
        if answer.body is not None and answer.post_id is not None and answer.parent_id is not None and answer.votes is not None:
            indexed_body = translate_latex(answer.body)
            #tags = data_reader.get_tags_for_answer_by_id(answer.parent_id) ignore tags for now since they lead to key errors

            yield {'docno': answer.post_id,
                   'text': indexed_body,
                   'origtext': answer.body,
                   'parentno': answer.parent_id,
                   'votes': answer.votes
                   }


def create_pyterrier_index(documents: List[Answer], index_name: str = "arqmath_indexV1"):
    index_path: str = f"{ROOT_DIRECTORY}./index/{index_name}"
    if not os.path.exists(index_path + "/data.properties"):
        indexer: IterDictIndexer = pt.IterDictIndexer(index_path, overwrite=True)
        index_reference: IndexRef = indexer.index(documents)
        pass
    else:
        index_reference: IndexRef = pt.IndexRef.of(index_path + "/data.properties")
        pass

    index = pt.IndexFactory.of(index_reference)
    return index
