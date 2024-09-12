from datetime import date

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import QHBoxLayout, QHeaderView, QMainWindow, QTableView, QVBoxLayout, QWidget

from src.backend.controllers import order_template_controller
from src.ui.models.order_template_view import OrderTemplateView

from ..utils.config import AppConfig
from .widgets.main_table import CenteredCheckboxDelegate, TableModel
from .widgets.table_bar import TableBar
from .widgets.toolbar import ToolBar
from .widgets.treeview import TreeView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(AppConfig.APP_NAME)
        self.setGeometry(200, 200, 1200, 900)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        central_widget.setLayout(layout)

        self.table_bar = TableBar()
        self.table_bar.on_period_changed = self.on_period_changed
        layout.addWidget(self.table_bar)

        self.treeview = self.create_treeview()
        self.table = self.create_table()

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.treeview)
        content_layout.addWidget(self.table, stretch=1)

        layout.addLayout(content_layout)

        self.create_toolbars()
        period = self.table_bar.get_period()
        self.load_data((period[0].toPyDate(), period[1].toPyDate()))

    def create_toolbars(self) -> None:
        self.bottombar = ToolBar(self, orientation=Qt.Orientation.Horizontal, style=Qt.ToolButtonStyle.ToolButtonIconOnly, icon_size=(30, 30))

        self.bottombar.add_separator()

        self.bottombar.add_button("Загрузить данные", AppConfig.get_resource_path("resources/assets/icons/windows/shell32-276.ico"), self.load_document)
        self.bottombar.add_button("Экспорт данных", AppConfig.get_resource_path("resources/assets/icons/windows/shell32-265.ico"), self.export_data)
        self.bottombar.add_button("Настройки", AppConfig.get_resource_path("resources/assets/icons/windows/shell32-315.ico"), self.settings_window)

        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.bottombar)

    def create_treeview(self) -> TreeView:
        return TreeView(self)

    def create_table(self) -> QTableView:
        return QTableView(self)

    def set_table_model(self) -> None:
        if self.data is None:
            return
        model = TableModel(self.data)
        self.table.setModel(model)
        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setColumnWidth(0, 10)
        self.table.setColumnWidth(1, 10)
        self.table.setItemDelegateForColumn(0, CenteredCheckboxDelegate(self.table))

    def set_tree_model(self) -> None:
        pass

    def on_period_changed(self, from_date: QDate, to_date: QDate) -> None:
        self.load_data((from_date.toPyDate(), to_date.toPyDate()))

    def load_data(self, period: tuple[date, date]) -> None:
        templates = order_template_controller.get_order_templates_by_period(period[0], period[1])
        self.data = [OrderTemplateView.from_order_template(template) for template in templates]
        self.set_table_model()
        self.set_tree_model()

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
