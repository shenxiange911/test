from __future__ import annotations
from typing import Dict, Any
from tools.gemini_client import GeminiClient, extract_text

def analyze_youtube(client: GeminiClient, youtube_url: str, prompt: str) -> Dict[str, Any]:
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"file_data": {"mime_type": "video/*", "file_uri": youtube_url}}
                ]
            }
        ]
    }
    result = client.generate_content(payload)
    return {"raw": result, "text": extract_text(result)}
