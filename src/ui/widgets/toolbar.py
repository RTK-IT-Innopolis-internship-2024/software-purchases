from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QSizePolicy, QToolBar, QWidget


class ToolBar(QToolBar):
    def __init__(
        self,
        parent,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        style: Qt.ToolButtonStyle = Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
        icon_size: tuple[int, int] = (32, 32),
    ) -> None:
        super().__init__(parent)
        self.actions_call: dict[str, QAction] = {}
        self.setOrientation(orientation)

        self.setToolButtonStyle(style)
        self.setIconSize(QSize(icon_size[0], icon_size[1]))

    def add_button(self, text: str, icon: str, trigger_action) -> None:
        self.actions_call[text] = QAction(QIcon(icon), text, self)
        self.actions_call[text].triggered.connect(trigger_action)
        self.addAction(self.actions_call[text])

    def add_separator(self) -> None:
        separator = QWidget(self)
        separator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(separator)
