from fastapi import BackgroundTasks, APIRouter
from fastapi.responses import FileResponse, JSONResponse
import os
import requests
import re

# Dev
from .audio.audio_request import AudioRequest
from .audio.audio_response import AudioResponse
from .audio.audio_download import AudioDownload
from .classes import UrlRequest

router = APIRouter()


@router.post("/iframe-sc/")
async def iframe_sc(request: UrlRequest) -> dict:
    try:
        url = request.url
        api = os.getenv("IFRAME_SC", "")
        default_response = {"message": "Hubo un error al cargar el reproductor."}

        if not api:
            return default_response

        response = requests.get(api, params={"url": url})

        if response.status_code != 200:
            print(f"Error al contactar con la API: {api}")
            return default_response

        data = response.json()
        code = data.get("code", "")

        match = re.search(r'src="(https://w\.soundcloud\.com/player/[^"]+)"', code)

        if match:
            src_url = match.group(1) + "&show_comments=false"
            return {"url": src_url}
        else:
            print("No se encontró el iframe de SoundCloud.")
            return default_response

    except Exception as e:
        print(f"Error en IFRAME-SC: {e}")
        return default_response


@router.post("/download-audio/")
async def download(audio_request: AudioRequest):
    audio_download = AudioDownload(**audio_request.model_dump())
    result: AudioResponse = await audio_download.extract()

    if result.error:
        return JSONResponse(status_code=406, content={"message": result.message})

    # borrar la carpeta luego de enviar el archivo
    background_tasks = BackgroundTasks()
    background_tasks.add_task(audio_download.cleanup)

    response = FileResponse(
        path=audio_download.file_path,
        media_type="audio/mpeg",
        filename=f"{result.title}",
        headers={
            "message": result.message if result.message else "",
        },
        background=background_tasks,
    )

    return response
