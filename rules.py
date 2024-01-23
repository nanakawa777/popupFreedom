from typing import Union

import pandas as pd
from pandas.io.parsers import TextFileReader
from rapidfuzz import fuzz


def load_data(filepath: str, chunk_size: int = None) -> Union[pd.DataFrame, TextFileReader]:
    """从CSV文件中加载数据

    设定 chunk_size 参数后，函数会返回一个可迭代的对象，你可以遍历此对象来逐块读取文件。
    Args:
        filepath:文件路径
        chunk_size: 块大小
    """
    return pd.read_csv(filepath, sep=',', header=0, usecols=["matchkey"], chunksize=chunk_size)


def run():
    df = pd.DataFrame(columns=['Text1', 'Text2', 'Score'])
    chunks = load_data("rules.csv", chunk_size=1000)
    for chunk in chunks:  # type: pd.DataFrame
        chunk.dropna(inplace=True)
        compared_value = chunk.iloc[0, 0]
        for value in chunk["matchkey"].to_list():
            score = fuzz.ratio(value, compared_value)
            new_record = {'Text1': compared_value, 'Text2': value, 'Score': round(score / 100.0, 7)}
            df = df.append(new_record, ignore_index=True)
        break
    df.to_csv('pretrain_data.csv', index=False)


if __name__ == '__main__':
    run()
