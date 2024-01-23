import os.path

from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
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

# 执行余弦相似搜索
similarities = cosine_similarity(queries, sentence_embeddings)
most_similar_sentence_idx = np.argmax(similarities, )
cosine_score = round(similarities[0][most_similar_sentence_idx], 3)
print(
    f"与【{sentence}】最相似的句子是【{sentences[most_similar_sentence_idx]}】\n"
    f"相似性得分为【{cosine_score:.3f}】\n"
)

# 执行语义搜索
# hit_score = 1
# hits = util.semantic_search(queries, sentence_embeddings, top_k=1)
# for hit in hits[0]:
#     print(f'句子: {sentences[hit["corpus_id"]]}, 相似度得分: {hit["score"]:.3f}')
#     hit_score = round(hit["score"], 3)
#     break
#
# score = round((cosine_score + hit_score) / 2, 3)

# 打印最相似的句子和相对应的相似性
if cosine_score < 0.90:
    print("未找到已配置的相似的规则")
