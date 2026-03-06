from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple
import re
import urllib.request
import urllib.parse

from core.media_types import guess_kind_from_path_or_url

URL_RE = re.compile(r"(https?://[^\s]+)", re.I)

def extract_urls(text: str) -> List[str]:
    return URL_RE.findall(text or "")

def is_url(s: str) -> bool:
    try:
        u = urllib.parse.urlparse(s)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except Exception:
        return False

def is_youtube(url: str) -> bool:
    u = urllib.parse.urlparse(url)
    host = (u.netloc or "").lower()
    return "youtube.com" in host or "youtu.be" in host

def head_content_type(url: str, timeout: int = 10) -> Tuple[Optional[str], Optional[int]]:
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ct = resp.headers.get("Content-Type")
            cl = resp.headers.get("Content-Length")
            return ct, int(cl) if cl and cl.isdigit() else None
    except Exception:
        # fallback: GET first byte
        req2 = urllib.request.Request(url, method="GET", headers={"Range": "bytes=0-0", "User-Agent": "mss/1.0"})
        try:
            with urllib.request.urlopen(req2, timeout=timeout) as resp:
                ct = resp.headers.get("Content-Type")
                cl = resp.headers.get("Content-Length")
                return ct, int(cl) if cl and cl.isdigit() else None
        except Exception:
            return None, None

def kind_from_mime(mime: Optional[str]) -> str:
    if not mime:
        return "unknown"
    m = mime.lower()
    if m.startswith("image/"):
        return "image"
    if m.startswith("video/"):
        return "video"
    if m.startswith("text/html"):
        return "page"
    return "unknown"

def download(url: str, out_dir: Path, timeout: int = 60) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    parsed = urllib.parse.urlparse(url)
    name = Path(parsed.path).name or "download.bin"
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", name)
    out = out_dir / safe
    req = urllib.request.Request(url, headers={"User-Agent": "mss/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        out.write_bytes(resp.read())
    return out

@dataclass
class ResolvedInput:
    kind: str                 # image | video | youtube | page | unknown
    source: str               # original string
    url: Optional[str] = None
    local_path: Optional[str] = None
    mime: Optional[str] = None

def resolve_inputs(user_text: str, work_inputs_dir: Path, also_inputs: Optional[List[str]] = None,
                   download_remote: bool = True) -> List[ResolvedInput]:
    items: List[str] = []
    items.extend(extract_urls(user_text))
    if also_inputs:
        items.extend(also_inputs)

    resolved: List[ResolvedInput] = []
    for raw in items:
        item = raw.strip().strip("()[]<>{}.,;"'")
        if not item:
            continue

        if is_url(item):
            if is_youtube(item):
                resolved.append(ResolvedInput(kind="youtube", source=item, url=item, local_path=None, mime="video/*"))
                continue

            ext_kind = guess_kind_from_path_or_url(item)
            ct, _ = head_content_type(item)
            mime_kind = kind_from_mime(ct)
            kind = mime_kind if mime_kind != "unknown" else ext_kind
            local = None
            if download_remote and kind in ("image", "video"):
                local = str(download(item, work_inputs_dir))
            resolved.append(ResolvedInput(kind=kind, source=item, url=item, local_path=local, mime=ct))
        else:
            p = Path(item)
            if p.exists() and p.is_file():
                kind = guess_kind_from_path_or_url(str(p))
                resolved.append(ResolvedInput(kind=kind, source=item, local_path=str(p.resolve())))
            else:
                resolved.append(ResolvedInput(kind="unknown", source=item))
    return resolved
