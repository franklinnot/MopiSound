import createFile from "../create-file";
import { api } from "./api";

export default async function downloadAudio(
  url: string,
  title: string | null,
  quality: string
): Promise<string | null> {
  if (!url) {
    return "Ingresa el link de la canción";
  }

  try {
    const response = await fetch(api.end_download_audio, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: url,
        title: title,
        quality: quality,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      let result = "";
      if (error.message) {
        result = error.message;
      } else if (error.detail && response.status == 429) {
        result = "Demasiadas solicitudes.";
      }
      return result;
    }

    if (!(await createFile(response))) {
      return "Hubo un error en la descarga";
    }

    return null;
  } catch {
    return "Hubo un error en la descarga.";
  }
}
