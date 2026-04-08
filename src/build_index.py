import pickle
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer

from src.ingest import ingest_data
from src.config import COLLECTION_NAME

# Init
client = QdrantClient(path="qdrant_db")  # LOCAL MODE ✅
model = SentenceTransformer("all-MiniLM-L6-v2")


def build_index():
    docs, structured = ingest_data()

    texts = []
    metadatas = []

    for text, meta in docs:
        texts.append(text)
        metadatas.append(meta)

    # Create collection
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

    # Generate embeddings
    embeddings = model.encode(texts)

    # Insert into Qdrant
    points = [
        PointStruct(
            id=i,
            vector=embeddings[i].tolist(),
            payload=metadatas[i]
        )
        for i in range(len(texts))
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    # Save BM25 + structured
    with open("bm25_corpus.pkl", "wb") as f:
        pickle.dump((texts, metadatas), f)

    with open("structured.pkl", "wb") as f:
        pickle.dump(structured, f)

    print("✅ Qdrant index built successfully")


if __name__ == "__main__":
    build_index()