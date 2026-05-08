from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
SETTINGS_PATH = BASE_DIR / "settings.json"

WINDOW_WIDTH = 160
WINDOW_HEIGHT = 160
TICK_INTERVAL_MS = 220
MOVE_STEP_PX = 2