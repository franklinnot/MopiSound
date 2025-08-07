import os
import uuid
import shutil
import yt_dlp
import asyncio
from pathlib import Path

from .audio_request import AudioRequest
from .audio_response import AudioResponse


class AudioDownload(AudioRequest):
    folder_path: str | os.PathLike[str] = "/"
    folder_name: str | None = None
    file_path: str | os.PathLike[str] = "/"
    file_name: str | None = None
    error: bool = False
    message: str = "Hubo un error en la descarga."
    output_dir: str = "downloads"
    cookies_file_path: str = "/code/app/cookies.txt"

    def get_info_opts(self) -> dict:
        return {
            # "quiet": True,
            # "no_warnings": True,
            "simulate": True,  # simular descarga
            "force_generic_extractor": True,  # metadatos generales
            "ie_key": "Generic",
            "cookiefile": self.cookies_file_path,
        }

    def get_down_opts(self, outtmpl: str) -> dict:
        return {
            "format": "bestaudio/best",  # la mejor pista de audio
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": self.quality,
                }
            ],
            "outtmpl": outtmpl,  # template para el nombre y ubicacion
            "noplaylist": True,  # no descargar listas de reproduccion
            # "quiet": True,  # no mostrar mensajes de progreso
            # "no_warnings": False,  # mostrar advertencias
            "ignoreerrors": True,  # evitar detener el proceso ante errores en la descarga
            "cookiefile": self.cookies_file_path,
        }

    async def verify_duration(self) -> None:
        # Duración máxima en horas según la calidad
        duration_limits = {
            "128": 4,  # baja calidad
            "192": 3,  # calidad media (por defecto)
            "256": 2,  # alta calidad
        }

        max_duration = duration_limits.get(self.quality, 3)  # fallback a 3
        
        try:
            ydl = yt_dlp.YoutubeDL(self.get_info_opts())
            info = await asyncio.to_thread(ydl.extract_info, self.url, download=False)
            ydl.close()

            if info is None:
                raise

            duration = info.get("duration")

            if duration is None:
                raise

            if duration > max_duration * 60 * 60:
                self.error = True
                self.message = (
                    f"La duración del video excede el límite de {max_duration} horas."
                )
            else:
                self.error = False
        except Exception as e:
            print(f"Error en verify_duration: {e}")
            self.error = True
            self.message = "No se pudo obtener información."

    async def setup(self) -> None:
        try:
            # creamos la carpeta  de descargas si no existe
            os.makedirs(self.output_dir, exist_ok=True)

            # creamos la carpeta que contendra el archivo de audio
            self.folder_name = str(uuid.uuid4())  # nombre unico
            # dentro de 'downloads'
            self.folder_path = os.path.join(self.output_dir, self.folder_name)
            os.makedirs(self.folder_path, exist_ok=True)  # creamos
        except Exception as e:
            print(f"Error en setup: {e}")
            self.error = True

    async def download_dlp(self) -> None:
        try:
            # crearemos el archivo dentro de la carpeta
            outtmpl = os.path.join(self.folder_path, "%(title)s.%(ext)s")

            ydl = yt_dlp.YoutubeDL(self.get_down_opts(outtmpl))
            await asyncio.to_thread(ydl.download, [self.url])
            ydl.close()

            # verificar si se creo el archivo
            file_exists = False
            for file in os.listdir(self.folder_path):
                if file.endswith(".mp3"):
                    self.file_path = Path(os.path.join(self.folder_path, file))
                    self.file_name = str(file)
                    file_exists = True
                    break

            if not file_exists:
                self.error = True
        except Exception as e:
            print(f"Error en download_dlp: {e}")
            self.error = True

    async def cleanup(self) -> None:
        try:
            if hasattr(self, "folder_path") and os.path.exists(self.folder_path):
                shutil.rmtree(self.folder_path)
                print(f"Carpeta de descarga limpiada: {self.folder_path}")
            elif hasattr(self, "file_path") and os.path.exists(self.file_path):
                os.remove(self.file_path)
                print(f"Archivo de audio limpiado: {self.file_path}")
        except Exception as e:
            print(f"Error al limpiar archivos temporales: {e}")

    async def extract(self) -> "AudioResponse":
        audio_response: AudioResponse = self.correct_url()

        if audio_response.error:
            return audio_response

        audio_response = self.verify_title()

        if audio_response.error:
            return audio_response

        await self.verify_duration()

        if not self.error:
            await self.setup()
            if not self.error:
                await self.download_dlp()
                if not self.error:
                    audio_response.title = self.title if self.title else self.file_name
                else:
                    await self.cleanup()
            else:
                await self.cleanup()

        if self.error:
            audio_response.message = self.message

        audio_response.error = self.error

        return audio_response
