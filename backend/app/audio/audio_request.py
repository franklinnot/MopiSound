from pydantic import BaseModel
from typing import Literal
from .audio_response import AudioResponse
from urllib.parse import urlparse
import re
from .services import Services


class AudioRequest(BaseModel):
    url: str
    title: str | None = None
    quality: Literal["128", "192", "256"] = "192"
    _service: Literal["youtube", "soundcloud"] = "youtube"

    def verify_domain(self) -> AudioResponse:
        domains_youtube = [
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "youtu.be",
        ]
        domains_soundcloud = [
            "soundcloud.com",
            "www.soundcloud.com",
            "m.soundcloud.com",
        ]

        audio_response = AudioResponse()
        try:
            parsed = urlparse(self.url)
            netloc = parsed.netloc.lower()
            invalid = True
            for domain in domains_youtube:
                if netloc.endswith(domain):
                    invalid = False
                    self._service = Services.YOUTUBE.value
                    break
            if invalid:
                for domain in domains_soundcloud:
                    if netloc.endswith(domain):
                        invalid = False
                        self._service = Services.SOUNDCLOUD.value
                        break

            audio_response.error = invalid
        finally:
            if audio_response.error:
                audio_response.message = (
                    "Solo se permiten enlaces de YouTube y SoundCloud."
                )
            return audio_response

    def verify_title(self) -> AudioResponse:
        audio_response = AudioResponse()
        invalid_chars = r'[<>:"/\\|?*\n\r\t]'

        if self.title is None or self.title.strip() == "":
            return audio_response
        elif re.search(invalid_chars, self.title):
            audio_response.error = True
            audio_response.message = "El título contiene caracteres no permitidos."
        elif len(self.title) > 48:
            audio_response.error = True
            audio_response.message = "El título es demasiado largo."

        return audio_response

    def correct_url(self) -> AudioResponse:
        """
        Si la URL es de YouTube y contiene múltiples parámetros,
        limpia todo excepto el parámetro 'v'.
        """
        audio_response: AudioResponse = self.verify_domain()

        if audio_response.error:
            return audio_response

        parsed = urlparse(self.url)
        if self._service == Services.YOUTUBE.value:
            video_id = None
            # URLs largas como youtube.com/watch?v=ID&...
            if "youtube.com" in parsed.netloc:
                match = re.search(r"[?&]v=([\w\-]{11})", self.url)
                if match:
                    video_id = match.group(1)

            # URLs cortas como youtu.be/ID?t=...
            elif "youtu.be" in parsed.netloc:
                path_match = re.match(r"^/([\w\-]{11})", parsed.path)
                if path_match:
                    video_id = path_match.group(1)

            if video_id:
                self.url = f"https://www.youtube.com/watch?v={video_id}"
            else:
                audio_response.error = True
                audio_response.message = "La URL de YouTube no es válida."

        return audio_response
