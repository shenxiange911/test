from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class Logger:
    logfile: Path

    def log(self, msg: str) -> None:
        ts = datetime.utcnow().isoformat(timespec="seconds")
        line = f"[{ts}] {msg}\n"
        self.logfile.parent.mkdir(parents=True, exist_ok=True)
        if self.logfile.exists():
            self.logfile.write_text(self.logfile.read_text(encoding="utf-8") + line, encoding="utf-8")
        else:
            self.logfile.write_text(line, encoding="utf-8")

def make_logger(log_dir: Path) -> Logger:
    log_dir.mkdir(parents=True, exist_ok=True)
    return Logger(log_dir / "run.log")
