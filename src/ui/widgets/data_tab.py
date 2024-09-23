from datetime import date

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QHBoxLayout, QHeaderView, QMessageBox, QTableView, QVBoxLayout, QWidget

from src.backend.controllers import order_template_controller
from src.ui.models.order_template_view import OrderTemplateView
from src.ui.models.order_view import OrderView
from src.ui.widgets.status_bar import StatusBar

from ...utils.config import AppConfig
from ..models.order_view import headers
from ..widgets.main_table import TableModel
from ..widgets.table_bar import TableBar
from ..widgets.treeview import TreeView


class DataTab(QWidget):
    def __init__(self, status_bar: StatusBar, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.status_bar = status_bar

        # Table Bar
        self.table_bar = TableBar()
        self.table_bar.on_period_changed = self.on_period_changed
        self.table_bar.on_refresh_document = self.on_refresh_clicked
        layout.addWidget(self.table_bar)

        # TreeView and Main Table
        self.treeview = self.create_treeview()
        self.treeview.on_state_changed = self.on_tree_updated
        self.table = self.create_table()

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.treeview)
        content_layout.addWidget(self.table, stretch=1)

        layout.addLayout(content_layout)
        self.period = self.table_bar.get_period_dates()

    def initialize(self) -> None:
        self.load_data()
        self.update_data(self.period)

    def create_treeview(self) -> TreeView:
        return TreeView(self)

    def create_table(self) -> QTableView:
        table = QTableView(self)
        font = table.font()
        font.setPointSize(AppConfig.FONT_SIZE)  # Increase font size
        table.setFont(font)
        return table

    def set_table_model(self, period: tuple[date, date], tree_data: dict) -> None:
        if self.data is None:
            return
        self.table.setModel(None)
        model = TableModel(self.data, period, tree_data)
        self.table.setModel(model)
        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            for i in range(1, len(headers) + 1):
                column = headers[i - 1]
                if column.width is not None:
                    self.table.setColumnWidth(i, column.width)
                else:
                    header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            header.setMaximumSectionSize(300)
            header.setStyleSheet(
                "::section { background-color: #f0f0f0; border-width: 1px; border-style: solid; border-color: #b0b0b0 #b0b0b0 #b0b0b0 #f0f0f0; }"
                "::section::first { background-color: #f0f0f0; border-width: 1px; border-style: solid; border-color: #b0b0b0 #b0b0b0 #b0b0b0 #b0b0b0; }"
            )

        vertical_header = self.table.verticalHeader()
        if vertical_header is not None:
            vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def set_tree_model(self, period: tuple[date, date]) -> None:
        if self.data is None:
            return
        self.treeview.populate_tree(self.data, period)

    def on_period_changed(self, from_date: QDate, to_date: QDate) -> None:
        self.period = (from_date.toPyDate(), to_date.toPyDate())
        self.update_data(self.period)

    def update_data(self, period: tuple[date, date]) -> None:
        self.set_tree_model(period)
        self.set_table_model(period, self.treeview.current_state)

    def on_tree_updated(self, tree_data: dict) -> None:
        self.set_table_model(self.period, tree_data)

    def load_data(self) -> None:
        template_files = order_template_controller.get_all_order_template_files()
        templates = []
        errors = []
        self.status_bar.update_status(0, len(template_files))
        for template_file in template_files:
            try:
                template = order_template_controller.get_order_template(template_file)
                templates.append(template)
                self.status_bar.update_status(len(templates), len(template_files))
            except ValueError as e:
                errors.append((template_file, str(e)))
            except PermissionError:
                error_msg = f"Нет доступа к файлу {template_file}.<br>Если файл открыт, закройте его и повторите попытку."
                errors.append((template_file, error_msg))
            except Exception as e:  # noqa: BLE001
                error_msg = f"Неизвестная ошибка при обработке файла {template_file}:<br>{e}"
                errors.append((template_file, error_msg))

        if len(errors) > 0:
            error_msg = "<br><br>".join([f"<b>{file}</b>:<br><span style='color:darkred;'>{error}</span>" for file, error in errors])
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные.<br><br>{error_msg}")
        self.data = [OrderTemplateView.from_order_template(template) for template in templates]

    def get_order_views_filtered(self) -> list[OrderView]:
        if self.data is None:
            return []

        tree_data = self.treeview.current_state
        orders: list[OrderView] = []
        for order_template in self.data:
            order_template_key = order_template.get_file_name()
            for order in order_template.orders_in_period(self.period[0], self.period[1]):
                order_key = order.get_key()
                if order_key in tree_data[order_template_key]["orders"] and tree_data[order_template_key]["orders"][order_key]["checked"]:
                    orders.append(order)

        return orders

    def on_refresh_clicked(self) -> None:
        self.load_data()
        self.update_data(self.period)
