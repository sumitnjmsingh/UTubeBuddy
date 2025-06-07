from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

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
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])

        if not transcript_text.strip():
            return QAResponse(answer="No transcript available for this video.")

        return QAResponse(answer="Transcript fetched successfully. Ready to add processing.")
    except TranscriptsDisabled:
        return QAResponse(answer="Transcripts are disabled for this video.")
    except Exception as e:
        return QAResponse(answer=f"Error: {str(e)}")