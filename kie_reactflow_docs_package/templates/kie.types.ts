export type KieProvider =
  | "market"
  | "4o-image"
  | "flux-kontext"
  | "runway"
  | "veo"
  | "suno";

export type SupportedModelKey =
  | "4o-image"
  | "flux-kontext-pro"
  | "flux-kontext-max"
  | "gpt-image-1.5-tti"
  | "gpt-image-1.5-iti"
  | "seedream-4.5-tti"
  | "seedream-4.5-edit"
  | "imagen4-fast"
  | "nano-banana-edit"
  | "runway-generate"
  | "veo3-fast"
  | "veo3-quality"
  | "kling-3-video"
  | "wan-2.6-i2v"
  | "sora2-i2v"
  | "elevenlabs-tts-multi-v2"
  | "elevenlabs-dialogue-v3"
  | "suno-generate";

export type SubmitTaskResult = {
  ok: boolean;
  taskId?: string;
  provider: KieProvider;
  error?: string;
};

export type NormalizedKieResult =
  | { kind: "image"; urls: string[]; previewUrl: string | null }
  | { kind: "video"; urls: string[]; previewUrl: string | null; resolution?: string }
  | {
      kind: "audio";
      urls: string[];
      previewUrl?: string | null;
      coverImageUrl?: string | null;
      streamUrl?: string | null;
    }
  | { kind: "text"; text: string };

export type KieTaskSnapshot = {
  taskId: string;
  status: string;
  provider: KieProvider;
  raw: unknown;
  normalized?: NormalizedKieResult;
};

export type UploadResult = {
  fileName: string;
  filePath: string;
  downloadUrl: string;
  fileSize?: number;
  mimeType?: string;
  uploadedAt?: string;
  expiresAt?: string;
};

export type FlowNodeRunState =
  | "idle"
  | "uploading"
  | "queued"
  | "generating"
  | "success"
  | "error";

export type FlowNodeData = {
  title: string;
  provider?: "kie";
  modelKey?: SupportedModelKey;
  runState: FlowNodeRunState;
  taskId?: string | null;
  error?: string | null;
  prompt?: string;
  uploads?: Array<{
    kind: "image" | "video" | "audio";
    source: "user" | "kie";
    originalName?: string;
    url: string;
    expiresAt?: string;
  }>;
  result?: NormalizedKieResult | null;
  providerMeta?: Record<string, unknown>;
};
