import shutil
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QHBoxLayout, QMainWindow, QMessageBox, QTabWidget, QVBoxLayout, QWidget

from src.backend.controllers import final_reports_controller
from src.ui.widgets.catalog_tab import CatalogsTab
from src.ui.widgets.data_tab import DataTab
from src.ui.widgets.status_bar import StatusBar
from src.utils import utils

from ..utils.config import AppConfig
from .widgets.toolbar import ToolBar


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(AppConfig.APP_NAME)
        self.setGeometry(200, 200, 1200, 900)
        central_widget = QWidget(self)
        self.status_bar = StatusBar(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        central_widget.setLayout(layout)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { font-size: 18px; }")
        layout.addWidget(self.tabs)

        # Add the first tab (DataTab)
        self.data_tab = DataTab(self.status_bar, self)
        self.tabs.addTab(self.data_tab, "Заявки")

        # Add the second tab (CatalogsTab)
        self.catalogs_tab = CatalogsTab(self)
        self.tabs.addTab(self.catalogs_tab, "Справочники")

        self.create_bottom_layout(layout)

    def initialize(self) -> None:
        self.data_tab.initialize()
        self.catalogs_tab.initialize()

    def create_bottom_layout(self, main_layout: QVBoxLayout) -> None:
        # Create a container widget for the bottom layout
        bottom_widget = QWidget(self)
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        # Create the status bar (on the left)
        bottom_layout.addWidget(self.status_bar)

        # Create the toolbar (on the right)
        self.bottombar = ToolBar(self, orientation=Qt.Orientation.Horizontal, style=Qt.ToolButtonStyle.ToolButtonIconOnly, icon_size=(30, 30))
        self.bottombar.add_separator()
        self.bottombar.add_button("Загрузить данные", AppConfig.get_resource_path("resources/assets/icons/windows/shell32-276.ico"), self.load_document)
        self.bottombar.add_button("Экспорт данных", AppConfig.get_resource_path("resources/assets/icons/windows/shell32-265.ico"), self.export_data)
        # SETTINGS: self.bottombar.add_button("Настройки", AppConfig.get_resource_path("resources/assets/icons/windows/shell32-315.ico"), self.settings_window)

        # Add the toolbar to the bottom layout (right side)
        bottom_layout.addWidget(self.bottombar)

        # Add the bottom layout to the main layout
        main_layout.addWidget(bottom_widget)

    def settings_window(self) -> None:
        """
        Event handler for the "Settings" button. Displays the "Settings" window.
        """

    def load_document(self) -> None:
        """
        Event handler for the "Load Data" button. Displays the "Load Data" dialog. Copies the selected files (may be multiple) to the "orders/orders_templates" folder.
        """
        order_files = QFileDialog.getOpenFileNames(self, "Выберите файлы", "", "Excel Files (*.xlsx *.xls)")[0]
        if len(order_files) == 0:
            return

        for order_file in order_files:
            order_template_path = AppConfig.get_order_path("orders/order_templates")
            try:
                shutil.copy(order_file, order_template_path)
            except shutil.SameFileError:
                QMessageBox.warning(self, "Ошибка", f"Файл {order_file} уже существует.")
            except PermissionError:
                QMessageBox.warning(self, "Ошибка", "Нет доступа к файлу.<br>Если файл открыт, закройте его и повторите попытку.")
            except Exception as e:  # noqa: BLE001
                QMessageBox.warning(self, "Ошибка", f"Не удалось скопировать файл.<br><span style='color:darkred;'>{e}</span>")

        self.data_tab.initialize()

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
            if file_path_str != "" and file_path and file_path.suffix == ".xlsx":
                file_path.parent.mkdir(parents=True, exist_ok=True)
                workbook.save(file_path)
            elif file_path_str != "":
                # error dialog
                QMessageBox.warning(self, "Ошибка", "Неверное расширение файла. Файл не будет сохранен.")
