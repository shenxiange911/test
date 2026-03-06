from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional
from tools.http import HttpClient

@dataclass
class GeminiClient:
    apiKey: str
    baseUrl: str
    model: str
    timeout: int = 120

    def generate_content(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.baseUrl}/v1beta/models/{self.model}:generateContent?key={self.apiKey}"
        http = HttpClient(timeout=self.timeout, retries=1, backoff_sec=0.8)
        status, res = http.request_json(url=url, method="POST", body=payload)
        if status >= 400:
            raise RuntimeError(f"Gemini HTTP {status}: {res}")
        return res

def extract_text(result: Dict[str, Any]) -> str:
    # Gemini standard: candidates[0].content.parts[0].text
    try:
        cand = result.get("candidates", [])[0]
        content = cand.get("content", {})
        parts = content.get("parts", [])
        if parts and "text" in parts[0]:
            return parts[0]["text"]
    except Exception:
        pass
    return ""
