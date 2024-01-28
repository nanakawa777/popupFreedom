from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
# model = SentenceTransformer('uer/sbert-base-chinese-nli')
query_embedding = model.encode('一个猪')
passage_embedding = model.encode(['一头猪', '一只猪'])

print("Similarity:", util.semantic_search(query_embedding, passage_embedding))
