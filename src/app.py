import os
import signal
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from .ui.main_window import MainWindow
from .utils.config import AppConfig


# https://stackoverflow.com/questions/4938723/what-is-the-correct-way-to-make-my-pyqt-application-quit-when-killed-from-the-co
def sigint_handler(*args):  # noqa: ARG001
    """Handler for the SIGINT signal."""
    sys.stderr.write("\r")
    QApplication.quit()


def run() -> int:
    """
    Initializes the application and runs it.
    """
    # set env variable QT_QPA_PLATFORM
    if os.name == "nt":
        os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"
    signal.signal(signal.SIGINT, sigint_handler)
    app: QApplication = QApplication(sys.argv)
    timer = QTimer()
    timer.start(1000)  # run every second
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.

    AppConfig.initialize()

    window: MainWindow = MainWindow()
    window.show()
    window.initialize()
    return sys.exit(app.exec())
