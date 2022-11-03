from arqmath_code.post_reader_record import DataReaderRecord
from arqmath_code.topic_file_reader import TopicReader


def init_data(task: int) -> (TopicReader, DataReaderRecord):
    topic_reader: TopicReader = TopicReader("../arqmath_dataset/Topics/Topics_Task1_2022_V0.1.xml")
    reader: DataReaderRecord = DataReaderRecord("../arqmath_dataset", ".V1.3")
    return topic_reader, reader
