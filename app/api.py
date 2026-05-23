from fastapi import FastAPI
from pydantic import BaseModel

from app.ingest import embed_text
from app.retriever import search
from app.llm import generate_answer

app = FastAPI()


class ChatRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    query_embedding = embed_text(req.question)
    results = search(query_embedding, top_k=5)
    context = "\n\n".join([row[0] for row in results])
    answer = generate_answer(context, req.question)

    return {
        "question": req.question,
        "answer": answer,
        "sources": [row[0][:200] for row in results],
    }