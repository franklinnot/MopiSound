import { api } from "./api";

export default async function getFramelyUrl(
  url: string
): Promise<string | null> {
  if (!url) {
    return null;
  }

  try {
    const response = await fetch(api.end_iframe_sc, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: url,
      }),
    });

    if (!response.ok) {
      return null;
    } else {
      const data = await response.json();
      return data.url;
    }
  } catch {
    return null;
  }
}
