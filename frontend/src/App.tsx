import { useState, useEffect } from "react";
import { FiRefreshCw } from "react-icons/fi";
import verifyDomain from "./utils/functions/verify-domain";
import downloadAudio from "./utils/functions/fetchs/download-audio";
import Loading from "./components/loading";
// youtube
import getVideoId from "get-video-id";
import LiteYouTubeEmbed from "react-lite-youtube-embed";
import "react-lite-youtube-embed/dist/LiteYouTubeEmbed.css";
// soundcloud
import getFramelyUrl from "./utils/functions/fetchs/iframe-sc";

function App() {
  const [data, setData] = useState({
    url: "",
    title: "",
    quality: "192",
    // para evitar recargar los iframes
    last_url: "",
    // para el estado de la request al back
    processing: false,
    // para los iframes
    id_youtube: "",
    url_framely: "",
    error: "",
  });

  const [details, setDetails] = useState(false);
  const [overflow, setOverflow] = useState(true);

  // manejar el overflow del body
  useEffect(() => {
    if (overflow || data.processing) {
      document.body.style.overflowY = "hidden";
      const duration = 300;

      const timer = setTimeout(() => {
        document.body.style.overflowY = "";
        setOverflow(false);
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [overflow, data.processing]);

  // recarga de iframes
  const handleNext = async () => {
    let isValid = false;
    let newIdYoutube = "";
    let newUrlFramely = "";

    if (data.url && verifyDomain(data.url)) {
      const video = getVideoId(data.url);

      if (video.id && video.service == "youtube") {
        newIdYoutube = video.id;
        newUrlFramely = "";
        isValid = true;
      } else {
        const framelyUrl = await getFramelyUrl(data.url);
        if (framelyUrl) {
          newUrlFramely = framelyUrl;
          newIdYoutube = "";
          isValid = true;
        }
      }
    }

    setData({
      ...data,
      last_url: data.url,
      id_youtube: newIdYoutube,
      url_framely: newUrlFramely,
      error: "",
    });

    if (isValid !== details) {
      setOverflow(true);
    }

    setDetails(isValid);
  };

  // descargar audio
  const handleDownload = async () => {
    if (data.processing) return;
    if (!data.last_url) {
      setData((prevData) => ({
        ...prevData,
        error: "Ingresa el link de la canción",
      }));
      return;
    }

    setData((prevData) => ({ ...prevData, processing: true }));
    const result = await downloadAudio(data.last_url, data.title, data.quality);

    if (result) {
      setData((prevData) => ({ ...prevData, error: result }));
    }

    setData((prevData) => ({ ...prevData, processing: false }));
  };

  return (
    <main
      className={`min-h-dvh grid place-items-center max-sm:px-8
                sm:py-6 md:py-12 transition-all duration-300 ease-in-out ${
                  !details
                    ? "max-sm:pb-40 sm:pb-52 md:pb-64 lg:pb-72"
                    : "max-sm:pb-3"
                }`}
    >
      <div
        className="w-full max-w-xl flex flex-col items-center 
                  max-sm:gap-6 sm:gap-8 relative pb-8"
      >
        {/* logo */}
        <img
          className={`max-sm:w-36 sm:w-44 md:w-48 lg:w-52 animate-glow-pulse 
                    max-sm:mb-5 sm:mb-6 md:mb-7 lg:mb-8 ${details && "hidden"}`}
          src="./icon.svg"
          alt="Logo de MOPI"
        />

        {/* frase - saludo */}
        <div
          className={`flex gap-2 items-center ${
            details ? "sm:mb-4 self-center" : "self-start"
          }`}
        >
          <img className="w-8" src="./icon.svg" alt="Logo de MOPI" />
          <h3
            className={`font-semibold tracking-wide title ${
              details ? "text-xl sm:text-2xl" : "text-base"
            }`}
          >
            Tu Música, Gratis
          </h3>
        </div>

        {/* input-url */}
        <div className="input_div">
          <label htmlFor="link">Link</label>
          <div className="flex gap-1.5">
            <input
              id="link"
              name="link"
              placeholder="https://www.youtube.com/..."
              value={data.url}
              onChange={(e) => {
                setData({ ...data, url: e.target.value.trim() });
              }}
              className="flex-grow"
              autoComplete="off"
              spellCheck="false"
            />
            {/* recargar iframe */}
            <button
              type="button"
              onClick={handleNext}
              className="px-3 grid place-items-center"
              disabled={data.url != "" && data.url == data.last_url}
            >
              <FiRefreshCw className="size-4" />
            </button>
          </div>
        </div>

        {details && (data.id_youtube || data.url_framely) && (
          <div className="w-full flex flex-col max-sm:gap-6 sm:gap-8 animate-fade-in">
            {/* titulo y bitrate */}
            <div className="w-full flex gap-1.5 max-sm:flex-col max-sm:gap-6">
              {/* input-title */}
              <div className="input_div">
                <label htmlFor="title">Título</label>
                <input
                  id="title"
                  name="title"
                  placeholder="Lipps Inc. - Funkytown"
                  value={data.title}
                  onChange={(e) => setData({ ...data, title: e.target.value })}
                  autoComplete="off"
                  spellCheck="false"
                  maxLength={48}
                />
              </div>

              {/* bitrate */}
              <div className="input_div sm:max-w-[148px]">
                <label htmlFor="quality">Calidad</label>
                <select
                  name="quality"
                  id="quality"
                  defaultValue={data.quality}
                  onChange={(e) =>
                    setData({ ...data, quality: e.target.value.trim() })
                  }
                >
                  <option value="128">Baja</option>
                  <option value="192">Media</option>
                  <option value="256">Alta</option>
                </select>
              </div>
            </div>

            {/* iframe - youtube */}
            {data.id_youtube && (
              <LiteYouTubeEmbed id={data.id_youtube} title="" />
            )}

            {/* iframe - soundcloud */}
            {data.url_framely && (
              <div className="soundcloud-container">
                <iframe
                  src={data.url_framely}
                  className="absolute top-0 left-0 w-full h-full border-0"
                  allowFullScreen
                  title="SoundCloud Player"
                />
              </div>
            )}

            {/* submit */}
            <button
              type="submit"
              className="w-full py-2 transition"
              disabled={data.processing}
              onClick={handleDownload}
            >
              Descargar
            </button>
            <span
              className="absolute max-sm:-bottom-12 sm:-bottom-11 md:-bottom-10
                        lg:-bottom-9 font-normal text-red-400"
            >
              {data.error}
            </span>
          </div>
        )}
      </div>
      <Loading isLoading={data.processing} />
    </main>
  );
}

export default App;
