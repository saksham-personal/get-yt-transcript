# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = FastAPI()

class TranscriptRequest(BaseModel):
    url: str

@app.post("/get-transcript/")
async def get_transcript(request: TranscriptRequest):
    try:
        video_id = re.search(r"(?:v=|be\/)([\w-]{11})", request.url).group(1)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([segment['text'] for segment in transcript])
        return {"transcript": full_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# For CORS if needed
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
