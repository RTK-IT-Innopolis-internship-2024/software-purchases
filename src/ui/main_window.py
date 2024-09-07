from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QTableView, QVBoxLayout
from ..utils.config import AppConfig
from .widgets.toolbar import ToolBar
from .widgets.treeview import TreeView
from .widgets.main_table import TableModel, CenteredCheckboxDelegate
from .widgets.table_bar import TableBar

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
        layout.addWidget(self.table_bar)

        self.treeview = self.create_treeview()
        self.table = self.create_table()

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.treeview)
        content_layout.addWidget(self.table, stretch=1)
        
        layout.addLayout(content_layout)

        self.create_toolbars()
        self.load_data()

    def create_toolbars(self) -> None:
        self.rightbar = ToolBar(self, orientation=Qt.Orientation.Vertical,
                                style=Qt.ToolButtonStyle.ToolButtonIconOnly,
                                icon_size=(30, 30))

        self.rightbar.add_separator()
    
        self.rightbar.add_button(
            "Загрузить данные", "resources/assets/icons/windows/shell32-276.ico", self.load_document)
        self.rightbar.add_button(
            "Экспорт данных", "resources/assets/icons/windows/shell32-265.ico", self.export_data)
        self.rightbar.add_button(
            "Настройки", "resources/assets/icons/windows/shell32-315.ico", self.settings_window)
        
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.rightbar)

    def create_treeview(self) -> TreeView:
        return TreeView(self)
    
    def create_table(self) -> QTableView:
        view = QTableView(self)
        return view
    
    def set_table_model(self):
        model = TableModel(self.data)
        self.table.setModel(model)
        self.table.setColumnWidth(0, 10)
        self.table.setColumnWidth(1, 10)
        self.table.setItemDelegateForColumn(0, CenteredCheckboxDelegate(self.table))

    def set_tree_model(self):
        #model = TreeModel(self.data)
        #self.treeview.load_model(model)
        pass
    
    def load_data(self):
        self.data = {
                'doc1': [
                [str(i) for i in range(20)],
                [str(i+20) for i in range(20)],
                [str(i+40) for i in range(20)],
            ]
        }
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
