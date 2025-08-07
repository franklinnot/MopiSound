import { useEffect, useState } from "react";

interface Props {
  isLoading: boolean;
}

export default function Loading({ isLoading }: Props) {
  const [shouldRender, setShouldRender] = useState(isLoading);
  const [isFadingOut, setIsFadingOut] = useState(false);

  useEffect(() => {
    let timer: NodeJS.Timeout;

    if (isLoading) {
      setShouldRender(true);
      setIsFadingOut(false);
    } else {
      if (shouldRender) {
        setIsFadingOut(true);
        timer = setTimeout(() => {
          setShouldRender(false);
        }, 300);
      }
    }
    return () => clearTimeout(timer);
  }, [isLoading, shouldRender]);

  if (!shouldRender) {
    return null;
  }

  const animationClass = isFadingOut ? "animate-fade-out" : "animate-fade-in";

  return (
    <div
      className={`absolute inset-0 grid place-items-center ${animationClass}`}
    >
      <div className="absolute inset-0 bg-neutral-900 opacity-95" />
      <img
        className="max-sm:size-52 sm:size-60 max-sm:mb-24 sm:mb-28 md:mb-32 
                  lg:mb-36 animate-glow-pulse"
        src="./icon.svg"
        alt="Logo de MOPI"
      />
    </div>
  );
}
