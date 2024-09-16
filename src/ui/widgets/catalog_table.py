from PyQt6.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt6.QtGui import QFont

from src.ui.models.column import TableColumn
from src.ui.models.view_model import ViewModel
from src.utils.config import AppConfig


class CatalogTableModel(QAbstractTableModel):
    def __init__(self, data: list[ViewModel], headers: list[TableColumn]) -> None:
        super().__init__()
        self.headers = headers
        self._data = [d.to_array() for d in data]

    def rowCount(self, _=None):  # noqa: N802
        return len(self._data)

    def columnCount(self, _=None):  # noqa: N802
        return len(self.headers) + 1

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
        return self.headers[section - 1].name

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        if index.column() == 0:
            return Qt.ItemFlag.ItemIsEnabled

        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
