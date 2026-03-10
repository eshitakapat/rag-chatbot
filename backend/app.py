from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
import shutil
import os
from groq import Groq

from ingest.ingest import extract_text_from_pdf, chunk_text
from vectorstore import store_chunks, search


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text)

    store_chunks(chunks)

    return {"chunks_created": len(chunks)}

@app.post("/chat")
async def chat(query: str):
    docs = search(query)
    context = "\n\n".join(docs)

    prompt = f"""
Answer using only this context:

{context}

Question: {query}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Answer strictly from provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return {"answer": response.choices[0].message.content}
