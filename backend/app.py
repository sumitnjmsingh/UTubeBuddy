from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from rag_pipeline import create_rag_pipeline
import logging
import uvicorn

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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QAResponse(BaseModel):
    answer: str

@app.get("/ask", response_model=QAResponse, summary="Ask a question based on a YouTube video's transcript")
async def ask_question(
    video_id: str = Query(..., description="YouTube video ID"),
    question: str = Query(..., description="User's question"),
) -> QAResponse:
    """
    Given a YouTube video ID and a question, fetches the transcript and answers the question using a RAG pipeline.
    """
    try:
        logger.info(f"Fetching transcript for video_id={video_id}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])

        if not transcript_text.strip():
            logger.warning("Transcript is empty.")
            return QAResponse(answer="No transcript available for this video.")

        logger.info("Transcript fetched successfully. Processing question...")
        answer = create_rag_pipeline(transcript_text, question)
        logger.info("Answer generated successfully.")
        return QAResponse(answer=answer or "No answer could be generated.")
    except TranscriptsDisabled:
        logger.warning(f"Transcripts disabled for video_id={video_id}")
        return QAResponse(answer="Transcripts are disabled for this video.")
    except Exception as e:
        logger.error(f"Error: {e}")
        return QAResponse(answer="An internal error occurred while processing your request.")
    
def start_server():
    """
    Starts the Uvicorn server.
    """
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False, workers=1)


if __name__ == "__main__":
    start_server()    