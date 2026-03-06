from __future__ import annotations
from typing import Dict, Any
from pathlib import Path
import base64
import os

from tools.gemini_client import GeminiClient, extract_text

_MIME = {
    ".jpg":"image/jpeg",".jpeg":"image/jpeg",".png":"image/png",".gif":"image/gif",".webp":"image/webp",
    ".mp4":"video/mp4",".mov":"video/quicktime",".avi":"video/x-msvideo",".webm":"video/webm",".mkv":"video/x-matroska"
}

def mime_for(path: Path) -> str:
    return _MIME.get(path.suffix.lower(), "application/octet-stream")

def analyze_local_media(client: GeminiClient, file_path: str, prompt: str) -> Dict[str, Any]:
    p = Path(file_path)
    data = base64.b64encode(p.read_bytes()).decode("utf-8")
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": mime_for(p), "data": data}}
                ]
            }
        ]
    }
    result = client.generate_content(payload)
    return {"raw": result, "text": extract_text(result)}
