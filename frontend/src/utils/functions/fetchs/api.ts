class Api {
  private url: string = "https://break.apimopi.top"; // http://localhost:8000/

  end_download_audio: string = this.url + "/download-audio/";
  end_iframe_sc: string = this.url + "/iframe-sc/";
}

export const api = new Api();
