from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QTabWidget, QVBoxLayout, QWidget

from src.backend.controllers import final_reports_controller
from src.ui.widgets.catalog_tab import CatalogsTab
from src.ui.widgets.data_tab import DataTab
from src.utils import utils

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
        start_date = self.data_tab.period[0]
        end_date = self.data_tab.period[1]

        start_year_quarter = utils.date_to_year_quarter(start_date)
        end_year_quarter = utils.date_to_year_quarter(end_date)

        folder_path = AppConfig.get_order_path("orders/final_reports")
        report_name = (
            f"Отчет о заявках за период - {start_year_quarter[0]} кв. {start_year_quarter[1]} - {end_year_quarter[0]} кв. {end_year_quarter[1]}.xlsx"
        )
        report_path = Path(f"{folder_path}/{report_name}")

        orders = [order_view.order for order_view in self.data_tab.get_order_views_filtered()]

        if len(orders) == 0:
            return

        sort_params = {"supervisor.name": True, "software.name": True, "tariff_plan": False, "is_new_license": True}
        try:
            workbook = final_reports_controller.create_orders_report_with_sort_by_params(orders, sort_params)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось создать отчет.\n{e}")
            return

        # display file dialog
        if workbook is not None:
            options = QFileDialog.Option.DontUseNativeDialog
            file_path_str, _ = QFileDialog.getSaveFileName(self, "Сохранить отчет", str(report_path), "Excel Files (*.xlsx)", options=options)
            file_path = Path(file_path_str)
            if file_path and file_path.suffix == ".xlsx":
                file_path.parent.mkdir(parents=True, exist_ok=True)
                workbook.save(file_path)
            else:
                # error dialog
                QMessageBox.warning(self, "Ошибка", "Неверное расширение файла. Файл не будет сохранен.")
