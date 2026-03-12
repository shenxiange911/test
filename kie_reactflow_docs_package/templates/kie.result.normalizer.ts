import type { NormalizedKieResult } from "./kie.types";

function safeParseJson(value: unknown) {
  if (typeof value !== "string") return value;
  try {
    return JSON.parse(value);
  } catch {
    return value;
  }
}

export function normalizeMarketTask(json: any): NormalizedKieResult | undefined {
  const data = json?.data;
  if (!data) return undefined;

  const resultJson = safeParseJson(data.resultJson);
  const urls: string[] = resultJson?.resultUrls || [];

  if (urls.length) {
    const first = urls[0];
    if (/\.mp4($|\?)/i.test(first)) {
      return { kind: "video", urls, previewUrl: first };
    }
    if (/\.(mp3|wav|m4a|aac|ogg)($|\?)/i.test(first)) {
      return { kind: "audio", urls, previewUrl: null, streamUrl: first };
    }
    return { kind: "image", urls, previewUrl: first };
  }

  return undefined;
}

export function normalize4oImageTask(json: any): NormalizedKieResult | undefined {
  const urls: string[] = json?.data?.response?.resultUrls || [];
  if (!urls.length) return undefined;
  return { kind: "image", urls, previewUrl: urls[0] };
}

export function normalizeVeoTask(json: any): NormalizedKieResult | undefined {
  const response = json?.data?.response;
  const urls: string[] = response?.resultUrls || [];
  if (!urls.length) return undefined;
  return {
    kind: "video",
    urls,
    previewUrl: urls[0],
    resolution: response?.resolution,
  };
}

export function normalizeSunoTask(json: any): NormalizedKieResult | undefined {
  const item = json?.data?.response?.sunoData?.[0];
  if (!item?.audioUrl) return undefined;
  return {
    kind: "audio",
    urls: [item.audioUrl],
    previewUrl: item?.imageUrl || null,
    coverImageUrl: item?.imageUrl || null,
    streamUrl: item?.streamAudioUrl || item.audioUrl,
  };
}
