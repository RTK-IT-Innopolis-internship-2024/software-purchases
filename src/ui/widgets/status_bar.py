from PyQt6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QWidget


class StatusBar(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Layout for the status bar
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Add a progress bar
        self.progress_bar = QProgressBar(self)
        # make smaller
        self.progress_bar.setFixedHeight(18)
        self.progress_bar.setFixedWidth(250)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMaximum(100)  # assuming 100% is the full range
        self.progress_bar.setValue(0)  # initial value
        self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #06B025; }")
        layout.addWidget(self.progress_bar)

        # Add a label for status text
        self.status_label = QLabel("", self)
        layout.addWidget(self.status_label)

    def update_status(self, current: int, total: int) -> None:
        """
        Updates the status of the progress bar and the status label.

        Args:
        ----
            current (int): The current number of files successfully uploaded.
            total (int): The total number of files to be uploaded.

        Returns:
        -------
            None

        """
        # Update the text and progress
        self.status_label.setText(f"Успешно загружено {current}/{total} файлов.")
        self.progress_bar.setValue(int((current / total) * 100) if total > 0 else 0)
