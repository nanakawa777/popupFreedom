import os.path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('uer/sbert-base-chinese-nli')
df = pd.read_csv("rules.csv", sep=',', header=0, usecols=["id", "matchkey"])
sentences = df["matchkey"].to_list()
if os.path.exists("sentence_embeddings.npy"):
    passage_embedding = np.load("sentence_embeddings.npy")
else:
    passage_embedding = model.encode(sentences)
    np.save("sentence_embeddings.npy", passage_embedding)

sentence = """所属应用：核心征管后端，异常原因：4510097000001001:纳税人在属期（2023-11-01,2023-12-31）内没有定期定额核定信息"""
query_embedding = model.encode(sentence, )

least_feature_scores = 0.93  # 最小特征分数
# 执行语义搜索
hits = util.semantic_search(query_embedding, passage_embedding, top_k=1)
for hit in hits[0]:
    if hit["score"] >= least_feature_scores:
        print(f'匹配: {sentences[hit["corpus_id"]]}, score: {hit["score"]:.3f}')
        break
else:
    print("No match found")
