from PySide6.QtWidgets import QApplication

from app.controller import AppController


def main() -> int:
    app = QApplication([])
    controller = AppController(app)
    controller.start()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())