from pathlib import Path

from PySide6.QtGui import QPixmap


class AssetLoader:
    def __init__(self, root: Path) -> None:
        self.root = root

    def load_resting(self) -> QPixmap:
        return QPixmap(str(self.root / "poses" / "resting" / "loaf.png"))

    def load_walking(self) -> list[QPixmap]:
        walk_dir = self.root / "poses" / "walking"
        frames = sorted(walk_dir.glob("walk_*.png"))
        return [QPixmap(str(frame)) for frame in frames]