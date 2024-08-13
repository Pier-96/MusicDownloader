from fastapi import FastAPI, Request, HTTPException
from pytube import YouTube
from pydub import AudioSegment
import os
import uuid

app = FastAPI()

def descargar_y_convertir_a_mp3(url, output_path=""):
    try:
        # Descargar el video de YouTube
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=output_path)

        # Convertir a MP3
        base, ext = os.path.splitext(out_file)
        mp3_file = base + '.mp3'

        # Utilizar pydub para convertir a MP3
        audio = AudioSegment.from_file(out_file)
        audio.export(mp3_file, format="mp3")

        # Eliminar el archivo original (opcional)
        os.remove(out_file)

        return mp3_file
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None

@app.get("/")
def read_root():
    return {"message": "API para descargar música de YouTube en formato MP3"}

@app.post("/download/")
async def download_music(request: Request):
    data = await request.json()
    url = data.get("url")

    if not url:
        raise HTTPException(status_code=400, detail="URL no proporcionada")

    # Descargar y convertir el video de YouTube a MP3
    file_path = descargar_y_convertir_a_mp3(url)

    if file_path:
        return {"message": "Descarga completa", "file": file_path}
    else:
        raise HTTPException(status_code=500, detail="Fallo en la descarga")