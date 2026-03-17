from store import store_chunks
print("INGEST STARTED")

import os
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_PATH = "data"

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    return splitter.split_text(text)


def ingest():

    print("Scanning data folder...")

    all_chunks = []

    for file in os.listdir(DATA_PATH):

        if file.endswith(".pdf"):

            file_path = os.path.join(DATA_PATH, file)

            print(f"Processing {file}")

            text = extract_text_from_pdf(file_path)

            chunks = chunk_text(text)

            print(f"{len(chunks)} chunks created")

            all_chunks.extend(chunks)

    print(f"\nTotal chunks created: {len(all_chunks)}")
    store_chunks(all_chunks)


if __name__ == "__main__":
    ingest()