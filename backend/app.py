from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="YouTube Transcript QnA API",
    description="Ask questions about YouTube videos using transcript-based retrieval-augmented generation (RAG).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QAResponse(BaseModel):
    answer: str

@app.get("/ask", response_model=QAResponse, summary="Ask a question based on a YouTube video's transcript")
async def ask_question(
    video_id: str = Query(..., description="YouTube video ID"),
    question: str = Query(..., description="User's question"),
) -> QAResponse:
    return QAResponse(answer="This is a placeholder answer.")