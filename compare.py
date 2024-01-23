import os.path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import paired_cosine_distances, cosine_similarity
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

sentence = """提示 业务执行失败,原因是:Could not get JDBC Connection; nested exception is weblogic.jdbc.extensions.PoolLimitSQLException: weblogic.common.resourcepool.ResourceLimitException: No resources currently available in pool jdbc/HxDataSource to allocate to applications, please increase the size of the pool and retry.. 确 认"""
queries = model.encode([sentence])
similarities = cosine_similarity(queries, sentence_embeddings)
most_similar_sentence_idx = np.argmax(similarities, )
score = round(similarities[0][most_similar_sentence_idx], 3)
# 打印最相似的句子和相对应的相似性
if score < 0.950:
    print("未找到已配置的相似的规则")
else:
    print(
        f"与【{sentence}】最相似的句子是【{sentences[most_similar_sentence_idx]}】\n"
        f"相似性得分为【{score:.3f}】\n"
        f"规则ID为【{df['id'].iloc[most_similar_sentence_idx]}】"
    )
