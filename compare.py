import os.path

from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np

model = SentenceTransformer('uer/sbert-base-chinese-nli')
df = pd.read_csv("rules.csv", sep=',', header=0, usecols=["id", "matchkey"], nrows=1000)
sentences = df["matchkey"].to_list()
if os.path.exists("sentence_embeddings.npy"):
    sentence_embeddings = np.load("sentence_embeddings.npy")
else:
    sentence_embeddings = model.encode(sentences, convert_to_tensor=True)
    np.save("sentence_embeddings.npy", sentence_embeddings)

sentence = """如您已完成申报，可忽略此信息"""
queries = model.encode([sentence], convert_to_tensor=True)


# 执行语义搜索
hits = util.semantic_search(queries, sentence_embeddings)
for hit in hits[0]:
    print(f'句子: {sentences[hit["corpus_id"]]}, 相似度得分: {hit["score"]:.3f}')
    break
