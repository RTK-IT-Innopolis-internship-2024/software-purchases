from datetime import date

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QHBoxLayout, QHeaderView, QTableView, QVBoxLayout, QWidget

from src.backend.controllers import order_template_controller
from src.ui.models.order_template_view import OrderTemplateView

from ...utils.config import AppConfig
from ..widgets.main_table import CenteredCheckboxDelegate, TableModel
from ..widgets.table_bar import TableBar
from ..widgets.treeview import TreeView


class DataTab(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Table Bar
        self.table_bar = TableBar()
        self.table_bar.on_period_changed = self.on_period_changed
        layout.addWidget(self.table_bar)

        # TreeView and Main Table
        self.treeview = self.create_treeview()
        self.table = self.create_table()

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.treeview)
        content_layout.addWidget(self.table, stretch=1)

        layout.addLayout(content_layout)

        # Initialize data load
        period = self.table_bar.get_period()
        self.load_data((period[0].toPyDate(), period[1].toPyDate()))

    def create_treeview(self) -> TreeView:
        return TreeView(self)

    def create_table(self) -> QTableView:
        table = QTableView(self)
        font = table.font()
        font.setPointSize(AppConfig.FONT_SIZE)  # Increase font size
        table.setFont(font)
        return table

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
        if self.data is None:
            return
        self.treeview.populate_tree(self.data)

    def on_period_changed(self, from_date: QDate, to_date: QDate) -> None:
        self.load_data((from_date.toPyDate(), to_date.toPyDate()))

    def load_data(self, period: tuple[date, date]) -> None:
        templates = order_template_controller.get_order_templates_by_period(period[0], period[1])
        self.data = [OrderTemplateView.from_order_template(template) for template in templates]
        self.set_table_model()
        self.set_tree_model()
