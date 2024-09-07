from PyQt6.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt6.QtWidgets import QTableView, QStyledItemDelegate
from PyQt6.QtGui import QFont

headers = ["Руководитель", 
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
           "Альтернативы"]

class CenteredCheckboxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        #option.state |= QStyle.State_Enabled
        option.rect.moveCenter(option.rect.center())  # Center align the checkbox within the rect
        super().paint(painter, option, index)

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        agg_data = []
        for doc, rows in data.items():
            agg_data.extend(rows)
        self._data = agg_data

        self.check_states = [Qt.CheckState.Unchecked] * len(self._data)  # Initialize all checkboxes to "unchecked"

    def rowCount(self, index):
        return len(self._data)
    
    def columnCount(self, parent):
        return len(headers) + 2
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return QVariant()

        row, column = index.row(), index.column()

        if column == 0:
            if role == Qt.ItemDataRole.CheckStateRole:
                return self.check_states[row]
            elif role == Qt.ItemDataRole.TextAlignmentRole:
                return Qt.AlignmentFlag.AlignCenter

        elif column == 1:
            if role == Qt.ItemDataRole.DisplayRole:
                return str(row + 1)
            elif role == Qt.ItemDataRole.FontRole:
                font = QFont()
                font.setBold(True)
                return font
            
        elif role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return str(self._data[row][column - 2])

        return QVariant()
    
    def headerData(self, section, orientation, role):
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return QVariant()

        if section == 0:
            return ""
        elif section == 1:
            return "#"
        else:
            return headers[section - 2]
    
    def setData(self, index, value, role):
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