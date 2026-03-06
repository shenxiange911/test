from __future__ import annotations
from pathlib import Path
import mimetypes
import urllib.parse

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".gif"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}

def guess_kind_from_path_or_url(path_or_url: str) -> str:
    p = urllib.parse.urlparse(path_or_url).path
    ext = Path(p).suffix.lower()
    if ext in IMAGE_EXT:
        return "image"
    if ext in VIDEO_EXT:
        return "video"
    return "unknown"

def guess_mime_from_path(path: str) -> str | None:
    return mimetypes.guess_type(path)[0]
