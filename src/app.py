import sys

from PyQt6.QtWidgets import QApplication

from .ui.main_window import MainWindow
from .utils.config import AppConfig


def run() -> int:
    """
    Initializes the application and runs it.
    """
    app: QApplication = QApplication(sys.argv)
    AppConfig.initialize()

    window: MainWindow = MainWindow()
    window.show()
    window.initialize()
    return app.exec()
