import json
from pathlib import Path
from typing import Any


DEFAULT_SETTINGS = {
    "window_x": 120,
    "window_y": 800,
    "scale_percent": 100,
}


class SettingsStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return DEFAULT_SETTINGS.copy()
        return {**DEFAULT_SETTINGS, **json.loads(self.path.read_text(encoding="utf-8"))}

    def save(self, settings: dict[str, Any]) -> None:
        self.path.write_text(
            json.dumps(settings, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )