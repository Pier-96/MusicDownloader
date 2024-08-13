from fastapi import FastAPI, Request
from pytube import YouTube
from pydub import AudioSegment
import os
import uuid

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API para descargar música de YouTube en formato MP3"}

@app.post("/download/")
async def download_music(request: Request):
    data = await request.json()
    url = data.get("url")

    if not url:
        return {"error": "URL no proporcionada"}

    # Descargar y convertir
    file_path = descargar_y_convertir_a_mp3(url)

    if file_path:
        return {"message": "Descarga completa", "file": file_path}
    else:
        return {"error": "Fallo en la descarga"}