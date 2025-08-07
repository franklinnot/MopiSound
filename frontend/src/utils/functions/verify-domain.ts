const domains = [
  "youtube.com",
  "www.youtube.com",
  "youtu.be",
  "m.youtube.com",
  "soundcloud.com",
  "www.soundcloud.com",
  "m.soundcloud.com",
];

export default function verifyDomain(url: string): boolean {
  try {
    const urlObject = new URL(url);
    const hostname = urlObject.hostname;

    if (domains.includes(hostname)) {
      return true;
    }
  } catch {
    return false;
  }
  return false;
}
