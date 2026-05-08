from collections.abc import Callable

from PySide6.QtCore import QPoint
from PySide6.QtGui import QAction, QCursor, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon


class TrayController:
    def __init__(self, app: QApplication, on_quit: Callable[[], None]) -> None:
        self.app = app
        self.menu = QMenu()
        self.tray = QSystemTrayIcon(self._default_icon(), app)

        quit_action = QAction("Exit", self.menu)
        quit_action.triggered.connect(on_quit)
        self.menu.addAction(quit_action)

        self.tray.setToolTip("Workmate")
        self.tray.setContextMenu(self.menu)

    def show(self) -> None:
        self.tray.show()

    def show_context_menu(self, position: QPoint | None = None) -> None:
        self.menu.popup(position or QCursor.pos())

    def _default_icon(self) -> QIcon:
        return self.app.style().standardIcon(QStyle.SP_ComputerIcon)