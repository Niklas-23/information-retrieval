import abc
from typing import List, Tuple

from arqmath_code.topic_file_reader import Topic
from arqmath_code.Entities.Post import Answer
from arqmath_code.post_reader_record import DataReaderRecord


class Pipeline(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'run') and
                callable(subclass.run) or
                NotImplemented)

    def __init__(self, data_reader: DataReaderRecord):
        """init all models"""
        self.data_reader = data_reader

    def __call__(self, queries: List[Topic]) -> List[Tuple[Topic, Answer, float]]:
        return self.run(queries=queries)

    @abc.abstractmethod
    def run(self, queries: List[Topic]) -> List[Tuple[Topic, Answer, float]]:
        """Chain all Models to complete the dataflow"""
        raise NotImplementedError
