from datetime import date
from typing import Any

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QStyledItemDelegate

from src.ui.models.order_template_view import OrderTemplateView
from src.utils.config import AppConfig

from ..models.order_view import headers


class CenteredCheckboxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.rect.moveCenter(option.rect.center())  # Center align the checkbox within the rect
        super().paint(painter, option, index)


class TableModel(QAbstractTableModel):
    def __init__(self, data: list[OrderTemplateView], period: tuple[date, date], tree_data: dict) -> None:
        super().__init__()
        agg_data = []
        for order_template in data:
            order_template_key = order_template.get_file_name()
            for order in order_template.orders_in_period(period[0], period[1]):
                order_key = order.get_key()
                if order_key in tree_data[order_template_key]["orders"] and tree_data[order_template_key]["orders"][order_key]["checked"]:
                    agg_data.append(order.to_array())

        self._data = agg_data

    def rowCount(self, _=None):  # noqa: N802
        return len(self._data)

    def columnCount(self, _=None):  # noqa: N802
        return len(headers) + 1

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            row, column = index.row(), index.column()

            if column == 0:
                if role == Qt.ItemDataRole.DisplayRole:
                    return str(row + 1)
                if role == Qt.ItemDataRole.FontRole:
                    font = QFont()
                    font.setBold(True)
                    return font

            elif role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
                return str(self._data[row][column - 1])

        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):  # noqa: N802
        if role == Qt.ItemDataRole.FontRole:
            font = QFont()
            font.setPointSize(AppConfig.FONT_SIZE)  # Increase font size
            return font

        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return QVariant()

        if section == 0:
            return "#"
        return headers[section - 1].name

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.ItemDataRole.EditRole):  # noqa: N802
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column() - 1] = value
            return True

        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        if index.column() == 0:
            return Qt.ItemFlag.ItemIsEnabled

        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
