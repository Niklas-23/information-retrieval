from collections import defaultdict

from arqmath_code.post_reader_record import DataReaderRecord
from arqmath_code.topic_file_reader import TopicReader
from src import init_data
from src.base.pipeline import Pipeline
from typing import Callable
import pandas as pd


class Runner:

    def __init__(self, pipeline: Callable[[DataReaderRecord], Pipeline], n=1, data_reader=None, topic_reader=None):
        if topic_reader is None or data_reader is None:
            self.topic_reader, self.data_reader = init_data(task=1)
        else:
            self.data_reader = data_reader
            self.topic_reader = topic_reader
        self.pipeline = pipeline(self.data_reader)
        self.n = n

    def run(self, path: str) -> pd.DataFrame:
        topics = list(self.topic_reader.map_topics.values())

        df: pd.DataFrame = pd.DataFrame()
        for i in range(self.n):
            data_run_i = self.pipeline(queries=topics)
            df_dict_i = defaultdict(list)
            for data_tuple in data_run_i:
                df_dict_i["Topic_Id"].append(data_tuple[0].topic_id)
                df_dict_i["Post_Id"].append(data_tuple[1].post_id)
                df_dict_i["Score"].append(data_tuple[2])
                df_dict_i["Run_Number"].append(i)
            df_i = pd.DataFrame(df_dict_i)
            df_i["Rank"] = df_i.sort_values(['Score']).groupby('Topic_Id').cumcount(ascending=False)
            df = pd.concat([df, df_i])
        df.to_csv(path, index=False, sep='\t')
        return df
