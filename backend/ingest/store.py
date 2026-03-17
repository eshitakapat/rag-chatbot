from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

DB_PATH = "db"

def store_chunks(chunks):

    print("Creating embeddings...")

    docs = [Document(page_content=c) for c in chunks]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = FAISS.from_documents(docs, embeddings)

    vectordb.save_local(DB_PATH)

    print("Vector database saved in db/")