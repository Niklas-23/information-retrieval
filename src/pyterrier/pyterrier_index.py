import os

import pyterrier as pt

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


def create_pyterrier_index(data_reader: DataReaderRecord, index_path: str = f"{ROOT_DIRECTORY}./index/arqmath_indexV1"):
    if not os.path.exists(index_path + "/data.properties"):
        indexer = pt.IterDictIndexer(index_path, overwrite=True)
        index_reference = indexer.index(get_arqmath_answers_as_iterable(data_reader))
        pass
    else:
        index_reference = pt.IndexRef.of(index_path + "/data.properties")
        pass

    index = pt.IndexFactor(index_reference)
    return index
