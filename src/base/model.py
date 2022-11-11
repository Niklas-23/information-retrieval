import abc
from typing import List, Union, Tuple
from arqmath_code.Entities.Post import Answer, Question
from arqmath_code.topic_file_reader import Topic


class Model(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'forward') and
                callable(subclass.forward) or
                NotImplemented)

    def __call__(self, queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[Tuple[Topic, Union[Question, Answer], float]]:
        return self.forward(queries=queries, documents=documents)

    @abc.abstractmethod
    def forward(self, queries: List[Topic], documents: List[Union[Question, Answer]]) -> List[Tuple[Topic, Union[Question, Answer], float]]:
        """Performs the models calculations on the data"""
        raise NotImplementedError
