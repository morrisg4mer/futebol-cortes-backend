from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp
import os
import uuid
import cv2
import numpy as np

app = FastAPI()

class VideoRequest(BaseModel):
    youtube_url: str

DOWNLOAD_DIR = "videos"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "ok"}

def detectar_movimento(video_path):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    prev_frame = None
    momentos = []

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray
            continue

        diff = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        movimento = np.sum(thresh)

        # valor empírico (funciona bem pra futebol)
        if movimento > 500000:
            segundo = int(frame_count / fps)
            momentos.append(segundo)

        prev_frame = gray
        frame_count += 1

    cap.release()

    # remove duplicados e ordena
    return sorted(list(set(momentos)))

@app.post("/processar")
def processar_video(data: VideoRequest):
    video_id = str(uuid.uuid4())
    video_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")

    ydl_opts = {
        "format": "mp4",
        "outtmpl": video_path,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([data.youtube_url])

    momentos = detectar_movimento(video_path)

    return {
        "status": "movimento_detectado",
        "momentos_em_segundos": momentos[:20]  # limita pra não explodir
    }
