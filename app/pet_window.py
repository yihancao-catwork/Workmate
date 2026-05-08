from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QMouseEvent, QPainter, QPixmap
from PySide6.QtWidgets import QWidget

from app.constants import WINDOW_HEIGHT, WINDOW_WIDTH


class PetWindow(QWidget):
    dragStarted = Signal()
    dragEnded = Signal()
    rightClicked = Signal()
    moved = Signal(int, int)

    def __init__(self) -> None:
        super().__init__()
        self.current_frame = QPixmap()
        self.dragging = False
        self.drag_offset = QPoint()

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def set_frame(self, pixmap: QPixmap) -> None:
        self.current_frame = pixmap
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        if not self.current_frame.isNull():
            painter.drawPixmap(self.rect(), self.current_frame)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.dragStarted.emit()
        elif event.button() == Qt.RightButton:
            self.rightClicked.emit()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.dragging:
            target = event.globalPosition().toPoint() - self.drag_offset
            self.move(target)
            self.moved.emit(target.x(), target.y())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.dragging:
            self.dragging = False
            self.dragEnded.emit()