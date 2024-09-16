from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget

from src.ui.widgets.catalog_tab import CatalogsTab
from src.ui.widgets.data_tab import DataTab

from ..utils.config import AppConfig
from .widgets.toolbar import ToolBar


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(AppConfig.APP_NAME)
        self.setGeometry(200, 200, 1200, 900)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        central_widget.setLayout(layout)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { font-size: 18px; }")
        layout.addWidget(self.tabs)

        # Add the first tab (DataTab)
        self.data_tab = DataTab(self)
        self.tabs.addTab(self.data_tab, "Заявки")

        # Add the second tab (CatalogsTab)
        self.catalogs_tab = CatalogsTab(self)
        self.tabs.addTab(self.catalogs_tab, "Справочники")

        self.create_toolbars()

    def create_toolbars(self) -> None:
        self.bottombar = ToolBar(self, orientation=Qt.Orientation.Horizontal, style=Qt.ToolButtonStyle.ToolButtonIconOnly, icon_size=(30, 30))

        self.bottombar.add_separator()

        self.bottombar.add_button("Загрузить данные", AppConfig.get_resource_path("resources/assets/icons/windows/shell32-276.ico"), self.load_document)
        self.bottombar.add_button("Экспорт данных", AppConfig.get_resource_path("resources/assets/icons/windows/shell32-265.ico"), self.export_data)
        self.bottombar.add_button("Настройки", AppConfig.get_resource_path("resources/assets/icons/windows/shell32-315.ico"), self.settings_window)

        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.bottombar)

    def settings_window(self) -> None:
        """
        Event handler for the "Settings" button. Displays the "Settings" window.
        """

    def load_document(self) -> None:
        """
        Event handler for the "Load Data" button. Displays the "Load Data" dialog.
        """

    def export_data(self) -> None:
        """
        Event handler for the "Export Data" button. Displays the "Export Data" dialog.
        """
