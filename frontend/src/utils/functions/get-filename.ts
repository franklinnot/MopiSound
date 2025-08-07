export default function getFilename(
  contentDisposition: string | null
): string | null {
  if (!contentDisposition) {
    return null;
  }

  let filename: string | null = null;

  const filenameStarMatch = /filename\*=(.+)/.exec(contentDisposition);
  if (filenameStarMatch && filenameStarMatch[1]) {
    try {
      const encodedFilename = filenameStarMatch[1];
      const parts = encodedFilename.split("''");
      if (parts.length > 1) {
        filename = decodeURIComponent(parts[1]);
      } else {
        filename = decodeURIComponent(encodedFilename);
      }
    } catch (e) {
      console.warn(e);
    }
  }

  if (!filename) {
    const simpleFilenameMatch = /filename="([^"]+)"/.exec(contentDisposition);
    if (simpleFilenameMatch && simpleFilenameMatch[1]) {
      filename = simpleFilenameMatch[1];
    }
  }

  return filename;
}
