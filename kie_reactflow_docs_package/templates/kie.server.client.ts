import type { SubmitTaskResult, UploadResult } from "./kie.types";

const KIE_API_BASE = "https://api.kie.ai";
const KIE_UPLOAD_BASE = "https://kieai.redpandaai.co";

function authHeaders(apiKey: string) {
  return {
    Authorization: `Bearer ${apiKey}`,
  };
}

export class KieServerClient {
  constructor(private apiKey: string) {}

  async uploadFileStream(file: Blob, fileName: string, uploadPath = "flow/uploads"): Promise<UploadResult> {
    const form = new FormData();
    form.append("file", file, fileName);
    form.append("uploadPath", uploadPath);
    form.append("fileName", fileName);

    const res = await fetch(`${KIE_UPLOAD_BASE}/api/file-stream-upload`, {
      method: "POST",
      headers: authHeaders(this.apiKey),
      body: form,
    });

    const json = await res.json();
    if (!res.ok || !json?.data) {
      throw new Error(json?.msg || "KIE file stream upload failed");
    }
    return json.data;
  }

  async uploadFileUrl(fileUrl: string, uploadPath = "flow/url-imports", fileName?: string): Promise<UploadResult> {
    const res = await fetch(`${KIE_UPLOAD_BASE}/api/file-url-upload`, {
      method: "POST",
      headers: {
        ...authHeaders(this.apiKey),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ fileUrl, uploadPath, fileName }),
    });

    const json = await res.json();
    if (!res.ok || !json?.data) {
      throw new Error(json?.msg || "KIE URL upload failed");
    }
    return json.data;
  }

  async submitMarketTask(payload: unknown): Promise<SubmitTaskResult> {
    const res = await fetch(`${KIE_API_BASE}/api/v1/jobs/createTask`, {
      method: "POST",
      headers: {
        ...authHeaders(this.apiKey),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const json = await res.json();
    return {
      ok: res.ok && !!json?.data?.taskId,
      taskId: json?.data?.taskId,
      provider: "market",
      error: !res.ok ? json?.msg || "Market submit failed" : undefined,
    };
  }

  async getMarketTask(taskId: string) {
    const res = await fetch(`${KIE_API_BASE}/api/v1/jobs/recordInfo?taskId=${encodeURIComponent(taskId)}`, {
      method: "GET",
      headers: authHeaders(this.apiKey),
    });
    return res.json();
  }

  async submit4oImage(payload: unknown): Promise<SubmitTaskResult> {
    const res = await fetch(`${KIE_API_BASE}/api/v1/gpt4o-image/generate`, {
      method: "POST",
      headers: {
        ...authHeaders(this.apiKey),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const json = await res.json();
    return {
      ok: res.ok && !!json?.data?.taskId,
      taskId: json?.data?.taskId,
      provider: "4o-image",
      error: !res.ok ? json?.msg || "4o image submit failed" : undefined,
    };
  }

  async get4oImage(taskId: string) {
    const res = await fetch(`${KIE_API_BASE}/api/v1/gpt4o-image/record-info?taskId=${encodeURIComponent(taskId)}`, {
      method: "GET",
      headers: authHeaders(this.apiKey),
    });
    return res.json();
  }

  async getDownloadUrl(url: string) {
    const res = await fetch(`${KIE_API_BASE}/api/v1/common/download-url`, {
      method: "POST",
      headers: {
        ...authHeaders(this.apiKey),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json?.msg || "download-url failed");
    return json.data as string;
  }

  async submitFluxKontext(payload: unknown): Promise<SubmitTaskResult> {
    const res = await fetch(`${KIE_API_BASE}/api/v1/flux/kontext/generate`, {
      method: "POST",
      headers: {
        ...authHeaders(this.apiKey),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    const json = await res.json();
    return {
      ok: res.ok && !!json?.data?.taskId,
      taskId: json?.data?.taskId,
      provider: "flux-kontext",
      error: !res.ok ? json?.msg || "Flux Kontext submit failed" : undefined,
    };
  }

  async getFluxKontext(taskId: string) {
    const res = await fetch(`${KIE_API_BASE}/api/v1/flux/kontext/record-info?taskId=${encodeURIComponent(taskId)}`, {
      method: "GET",
      headers: authHeaders(this.apiKey),
    });
    return res.json();
  }

  async submitRunway(payload: unknown): Promise<SubmitTaskResult> {
    const res = await fetch(`${KIE_API_BASE}/api/v1/runway/generate`, {
      method: "POST",
      headers: {
        ...authHeaders(this.apiKey),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    const json = await res.json();
    return {
      ok: res.ok && !!json?.data?.taskId,
      taskId: json?.data?.taskId,
      provider: "runway",
      error: !res.ok ? json?.msg || "Runway submit failed" : undefined,
    };
  }

  async getRunway(taskId: string) {
    const res = await fetch(`${KIE_API_BASE}/api/v1/runway/record-info?taskId=${encodeURIComponent(taskId)}`, {
      method: "GET",
      headers: authHeaders(this.apiKey),
    });
    return res.json();
  }

  async submitVeo(payload: unknown): Promise<SubmitTaskResult> {
    const res = await fetch(`${KIE_API_BASE}/api/v1/veo/generate`, {
      method: "POST",
      headers: {
        ...authHeaders(this.apiKey),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    const json = await res.json();
    return {
      ok: res.ok && !!json?.data?.taskId,
      taskId: json?.data?.taskId,
      provider: "veo",
      error: !res.ok ? json?.msg || "Veo submit failed" : undefined,
    };
  }

  async getVeo(taskId: string) {
    const res = await fetch(`${KIE_API_BASE}/api/v1/veo/record-info?taskId=${encodeURIComponent(taskId)}`, {
      method: "GET",
      headers: authHeaders(this.apiKey),
    });
    return res.json();
  }

  async submitSuno(payload: unknown): Promise<SubmitTaskResult> {
    const res = await fetch(`${KIE_API_BASE}/api/v1/generate`, {
      method: "POST",
      headers: {
        ...authHeaders(this.apiKey),
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    const json = await res.json();
    return {
      ok: res.ok && !!json?.data?.taskId,
      taskId: json?.data?.taskId,
      provider: "suno",
      error: !res.ok ? json?.msg || "Suno submit failed" : undefined,
    };
  }

  async getSuno(taskId: string) {
    const res = await fetch(`${KIE_API_BASE}/api/v1/generate/record-info?taskId=${encodeURIComponent(taskId)}`, {
      method: "GET",
      headers: authHeaders(this.apiKey),
    });
    return res.json();
  }
}
