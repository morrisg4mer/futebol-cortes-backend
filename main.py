from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class VideoRequest(BaseModel):
    youtube_url: str

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/processar")
def processar_video(data: VideoRequest):
    return {
        "status": "recebido",
        "youtube_url": data.youtube_url
    }
