import pickle
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

from src.config import COLLECTION_NAME

# Init
client = QdrantClient(path="qdrant_db")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load BM25
with open("bm25_corpus.pkl", "rb") as f:
    texts, metadatas = pickle.load(f)

tokenized_corpus = [t.split() for t in texts]
bm25 = BM25Okapi(tokenized_corpus)


def vector_search(query, k=5):
    query_vec = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vec,
        limit=k
    )

    return [
        (texts[r.id], metadatas[r.id])
        for r in results.points
    ]


# 🔥 HYBRID SEARCH
def hybrid_search(query, k=5):
    vector_results = vector_search(query, k)

    tokenized_query = query.split()
    scores = bm25.get_scores(tokenized_query)

    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

    keyword_results = [(texts[i], metadatas[i]) for i in top_idx]

    return vector_results + keyword_results


# 🔥 RERANK
def rerank(query, docs, llm, top_k=5):
    scored = []

    for content, meta in docs:
        prompt = f"""
Score relevance (0-10):

Query: {query}
Doc: {content[:300]}
"""
        try:
            score = float(llm.invoke(prompt).content.strip())
        except:
            score = 0

        scored.append((score, content, meta))

    scored.sort(reverse=True)
    return scored[:top_k]