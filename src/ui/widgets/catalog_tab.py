import typing

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QHeaderView, QListWidget, QMessageBox, QTableView, QWidget

if typing.TYPE_CHECKING:
    from src.ui.models.column import TableColumn
    from src.ui.models.view_model import ViewModel

from src.backend.controllers import order_template_controller
from src.ui.models.company_view import CompanyView
from src.ui.models.country_view import CountryView
from src.ui.models.license_type_view import LicenseTypeView
from src.ui.models.software_class_view import SoftwareClassView
from src.ui.models.software_view import SoftwareView
from src.ui.models.supervisor_view import SupervisorView
from src.ui.widgets.catalog_table import CatalogTableModel

from ...utils.config import AppConfig


class HeaderView(QHeaderView):
    def __init__(self, parent=None) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent)


class CatalogsTab(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)

        self.data: dict[str, tuple[list[ViewModel], list[TableColumn]]] = {}

        # Create catalog item list
        self.catalog_list = QListWidget()
        font = self.catalog_list.font()
        font.setPointSize(AppConfig.FONT_SIZE)  # Increase font size
        self.catalog_list.setFont(font)
        self.catalog_list.currentItemChanged.connect(self.on_catalog_selected)
        layout.addWidget(self.catalog_list)

        # Create table for the selected catalog
        self.catalog_table = QTableView()
        layout.addWidget(self.catalog_table, stretch=1)

    def initialize(self) -> None:
        self.load_data()
        self.load_catalogs()

    def load_data(self) -> None:
        errors = []
        try:
            template = order_template_controller.get_main_order_template()  # TODO: merge from all templates
        except ValueError as e:
            errors.append(str(e))
        except PermissionError:
            error_msg = "Нет доступа к файлу основного шаблона.\nЕсли файл открыт, закройте его и повторите попытку."
            errors.append(error_msg)
        except Exception as e:  # noqa: BLE001
            error_msg = f"Неизвестная ошибка при обработке файла основного шаблона:\n{e}"
            errors.append(error_msg)

        if len(errors) > 0:
            error_msg = errors[0]
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные из основного шаблона.\n\n{error_msg}")

        if template is None:
            self.data = {}

        self.data = {
            "Проекты": ([CompanyView.from_company(c) for c in template.companies], CompanyView.get_headers()),
            "Страны": ([CountryView.from_country(c) for c in template.countries], CountryView.get_headers()),
            "Руководители": ([SupervisorView.from_supervisor(s) for s in template.supervisors], SupervisorView.get_headers()),
            "Типы лицензий": ([LicenseTypeView.from_license_type(lt) for lt in template.license_type], LicenseTypeView.get_headers()),
            "Классы программного обеспечения": (
                [SoftwareClassView.from_software_class(sc) for sc in template.software_classes],
                SoftwareClassView.get_headers(),
            ),
            "Программное обеспечение": ([SoftwareView.from_software(s) for s in template.software_list], SoftwareView.get_headers()),
        }

    def load_catalogs(self) -> None:
        """
        Load catalog items into the list.
        """
        # Simulated catalog items
        catalogs = self.data.keys()
        for catalog in catalogs:
            self.catalog_list.addItem(catalog)

    def on_catalog_selected(self) -> None:
        """
        Event handler when a catalog is selected from the list.
        """
        selected_catalog = self.catalog_list.currentItem()
        if selected_catalog is None:
            return
        self.load_catalog_table(selected_catalog.text())

    def load_catalog_table(self, catalog_name: str) -> None:
        """
        Load data into the catalog table based on the selected catalog.
        """
        self.catalog_table.setModel(None)
        headers = self.data[catalog_name][1]
        data = self.data[catalog_name][0]

        catalog_model = CatalogTableModel(data, headers)
        self.catalog_table.setModel(catalog_model)

        # Set font size for the table
        font = self.catalog_table.font()
        font.setPointSize(AppConfig.FONT_SIZE)  # Increase font size
        self.catalog_table.setFont(font)

        # Resize columns
        table_header = self.catalog_table.horizontalHeader()
        if table_header is not None:
            table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            for i in range(1, len(headers) + 1):
                column = headers[i - 1]
                if column.width is not None:
                    self.catalog_table.setColumnWidth(i, column.width)
                else:
                    table_header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
            table_header.setMaximumSectionSize(300)
            table_header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap)
            max_height_multiplier = 1.0
            for i in range(1, len(headers) + 1):
                column = headers[i - 1]
                if column.height_multiplier is not None:
                    max_height_multiplier = max(max_height_multiplier, column.height_multiplier)
            table_header.setMinimumHeight(int(30 * max_height_multiplier))
            table_header.setStyleSheet(
                "::section { background-color: #f0f0f0; border-width: 1px; border-style: solid; border-color: #b0b0b0 #b0b0b0 #b0b0b0 #f0f0f0; }"
                "::section::first { background-color: #f0f0f0; border-width: 1px; border-style: solid; border-color: #b0b0b0 #b0b0b0 #b0b0b0 #b0b0b0; }"
            )

        vertical_header = self.catalog_table.verticalHeader()
        if vertical_header is not None:
            vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
