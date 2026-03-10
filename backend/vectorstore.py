import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.get_or_create_collection("docs")

model = SentenceTransformer("all-MiniLM-L6-v2")

def store_chunks(chunks):
    embeddings = model.encode(chunks).tolist()

    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

def search(query, k=5):
    q_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=q_embedding,
        n_results=k
    )

    return results["documents"][0]
