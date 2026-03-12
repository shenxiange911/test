import fs from "node:fs";
import path from "node:path";
import { pipeline } from "node:stream/promises";

export async function persistRemoteMedia(params: {
  url: string;
  dir: string;
  filename: string;
}) {
  const { url, dir, filename } = params;
  await fs.promises.mkdir(dir, { recursive: true });

  const res = await fetch(url);
  if (!res.ok || !res.body) {
    throw new Error(`Failed to download media: ${res.status}`);
  }

  const filePath = path.join(dir, filename);
  const stream = fs.createWriteStream(filePath);
  await pipeline(res.body as any, stream);

  return {
    filePath,
    filename,
  };
}

export async function downloadInBrowser(url: string, filename: string) {
  const res = await fetch(url);
  const blob = await res.blob();
  const objectUrl = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = objectUrl;
  a.download = filename;
  a.click();

  URL.revokeObjectURL(objectUrl);
}
