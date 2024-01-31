import os.path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util

model_path = r"d:\torch\sentence_transformers\uer_sbert-base-chinese-nli"
least_feature_scores = 0.93  # 最小特征分数
if os.path.exists(model_path):
    print("本地加载model")
    model = SentenceTransformer(model_path)
else:
    print("下载并加载model")
    model = SentenceTransformer('uer/sbert-base-chinese-nli')

print("读取数据")
df = pd.read_csv("rules.csv", sep=',', header=0, usecols=["id", "matchkey"], keep_default_na=False)
sentences = df["matchkey"].to_list()
if os.path.exists("sentence_embeddings.npy"):
    print("读取npy")
    passage_embedding = np.load("sentence_embeddings.npy")
else:
    print("生成npy")
    passage_embedding = model.encode(sentences, convert_to_tensor=True)
    print("保存npy")
    np.save("sentence_embeddings.npy", passage_embedding)


def semantic_search(sentence: str):
    query_embedding = model.encode(sentence, convert_to_tensor=True)
    # 执行语义搜索
    hits = util.semantic_search(query_embedding, passage_embedding, top_k=1)
    for hit in hits[0]:
        if hit["score"] >= least_feature_scores:
            file({
                "content": sentence,
                "match": sentences[hit["corpus_id"]],
                "score": hit["score"]
            })
            return df["id"].iloc[hit["corpus_id"]]


def file(data):
    """归档比对结果"""
    pd.DataFrame([data]).to_csv('file.csv', mode='a', header=False, index=False, )
