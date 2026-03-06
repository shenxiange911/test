from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
import json
import time
import urllib.request
import urllib.error

@dataclass
class HttpClient:
    timeout: int = 60
    retries: int = 2
    backoff_sec: float = 0.8

    def request_json(self, url: str, method: str = "POST", body: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> Tuple[int, Any]:
        data = None
        hdrs = {"Content-Type": "application/json", "User-Agent": "mss/1.0"}
        if headers:
            hdrs.update(headers)

        if body is not None:
            data = json.dumps(body).encode("utf-8")

        last_err = None
        for attempt in range(self.retries + 1):
            try:
                req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    raw = resp.read().decode("utf-8", errors="replace")
                    try:
                        return resp.status, json.loads(raw)
                    except Exception:
                        return resp.status, raw
            except urllib.error.HTTPError as e:
                last_err = (e.code, e.read().decode("utf-8", errors="replace"))
            except Exception as e:
                last_err = (-1, str(e))

            if attempt < self.retries:
                time.sleep(self.backoff_sec * (2 ** attempt))
        # give up
        code, msg = last_err if last_err else (-1, "unknown error")
        return int(code), {"error": msg}
