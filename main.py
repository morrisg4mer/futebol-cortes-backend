from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp
import os
import uuid

app = FastAPI()

class VideoRequest(BaseModel):
    youtube_url: str

DOWNLOAD_DIR = "videos"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/processar")
def processar_video(data: VideoRequest):
    video_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

    ydl_opts = {
        "format": "mp4",
        "outtmpl": output_path,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([data.youtube_url])

    return {
        "status": "baixado",
        "arquivo": output_path
    }
