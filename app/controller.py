from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from app.asset_loader import AssetLoader
from app.constants import ASSETS_DIR, MOVE_STEP_PX, SETTINGS_PATH, TICK_INTERVAL_MS
from app.pet_window import PetWindow
from app.settings import SettingsStore
from app.state_machine import PetState, PetStateMachine
from app.tray import TrayController


class AppController:
    def __init__(self, app: QApplication) -> None:
        self.app = app
        self.settings_store = SettingsStore(SETTINGS_PATH)
        self.settings = self.settings_store.load()

        self.assets = AssetLoader(ASSETS_DIR)
        self.rest_frame = self.assets.load_resting()
        self.walk_frames = self.assets.load_walking()

        self.state_machine = PetStateMachine()
        self.window = PetWindow()
        self.tray = TrayController(app, on_quit=app.quit)
        self.frame_index = 0
        self.direction = 1

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

        self.window.dragStarted.connect(self.state_machine.start_drag)
        self.window.dragEnded.connect(self.state_machine.end_drag)
        self.window.moved.connect(self.on_window_moved)
        self.window.rightClicked.connect(self.show_window_menu)

    def start(self) -> None:
        self.window.move(self.settings["window_x"], self.settings["window_y"])
        self.window.set_frame(self.rest_frame)
        self.window.show()
        self.tray.show()
        self.state_machine.start_walking()
        self.timer.start(TICK_INTERVAL_MS)

    def tick(self) -> None:
        if self.state_machine.state == PetState.DRAGGED:
            return

        if self.state_machine.state == PetState.WALKING and self.walk_frames:
            self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
            self.window.set_frame(self.walk_frames[self.frame_index])
            self._move_window()
            return

        self.window.set_frame(self.rest_frame)

    def on_window_moved(self, x: int, y: int) -> None:
        self.settings["window_x"] = x
        self.settings["window_y"] = y
        self.settings_store.save(self.settings)

    def show_window_menu(self) -> None:
        self.tray.show_context_menu()

    def _move_window(self) -> None:
        screen = self.app.primaryScreen()
        if screen is None:
            self.window.move(self.window.x() + MOVE_STEP_PX * self.direction, self.window.y())
            return

        available_geometry = screen.availableGeometry()
        next_x = self.window.x() + MOVE_STEP_PX * self.direction
        right_edge = next_x + self.window.width()

        if next_x <= available_geometry.left() or right_edge >= available_geometry.right():
            self.direction *= -1
            next_x = self.window.x() + MOVE_STEP_PX * self.direction

        self.window.move(next_x, self.window.y())