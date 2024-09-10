from typing import Any

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QStyledItemDelegate

headers = [
    "Руководитель",
    "Сотрудник",
    "Наименование ПО",
    "Производитель ПО",
    "Тарифный план",
    "Логин и пароль",
    "Страна производства",
    "Количество",
    "Продление/новая",
    "Цена за единицу",
    "Стоимость",
    "Окончание срока действия текущих лицензий",
    "Лицензия",
    "Срок полезного использования",
    "Тип ПО по классификатору Минкомсвязи",
    "Наличие в реестре",
    "Наличие аналогов",
    "Проект",
    "Ссылка",
    "Альтернативы",
]


class CenteredCheckboxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.rect.moveCenter(option.rect.center())  # Center align the checkbox within the rect
        super().paint(painter, option, index)


class TableModel(QAbstractTableModel):
    def __init__(self, data) -> None:
        super().__init__()
        agg_data = []
        for rows in data.values():
            agg_data.extend(rows)
        self._data = agg_data

        self.check_states = [Qt.CheckState.Unchecked] * len(self._data)  # Initialize all checkboxes to "unchecked"

    def rowCount(self, _=None):  # noqa: N802
        return len(self._data)

    def columnCount(self, _=None):  # noqa: N802
        return len(headers) + 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            row, column = index.row(), index.column()

            if column == 0:
                if role == Qt.ItemDataRole.CheckStateRole:
                    return self.check_states[row]
                if role == Qt.ItemDataRole.TextAlignmentRole:
                    return Qt.AlignmentFlag.AlignCenter

            elif column == 1:
                if role == Qt.ItemDataRole.DisplayRole:
                    return str(row + 1)
                if role == Qt.ItemDataRole.FontRole:
                    font = QFont()
                    font.setBold(True)
                    return font

            elif role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
                return str(self._data[row][column - 2])

        return QVariant()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):  # noqa: N802
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return QVariant()

        if section == 0:
            return ""
        if section == 1:
            return "#"
        return headers[section - 2]

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.ItemDataRole.EditRole):  # noqa: N802
        if role == Qt.ItemDataRole.EditRole:
            try:
                value = int(value)
            except ValueError:
                return False
            self._data[index.row()][index.column() - 2] = value
            return True

        # Handle checkbox state changes
        if role == Qt.ItemDataRole.CheckStateRole and index.column() == 0:
            self.check_states[index.row()] = value
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.CheckStateRole])
            return True

        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        if index.column() == 0:
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable

        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
