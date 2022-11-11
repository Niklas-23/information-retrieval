import abc
from typing import List, Tuple

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

    @abc.abstractmethod
    def run(self) -> List[Tuple[Answer, float]]:
        """Chain all Models to complete the dataflow"""
        raise NotImplementedError
