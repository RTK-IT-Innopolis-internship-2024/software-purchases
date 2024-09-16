import typing

from PyQt6.QtWidgets import QHBoxLayout, QHeaderView, QListWidget, QTableView, QWidget

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


class CatalogsTab(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)

        self.data: dict[str, tuple[list[ViewModel], list[TableColumn]]] = {}
        self.load_data()

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

        self.load_catalogs()

    def load_data(self) -> None:
        template = order_template_controller.get_main_order_template()  # TODO: merge from all templates

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
        headers = self.data[catalog_name][1]
        data = self.data[catalog_name][0]

        catalog_model = CatalogTableModel(data, headers)
        self.catalog_table.setModel(catalog_model)

        # Set font size for the table
        font = self.catalog_table.font()
        font.setPointSize(AppConfig.FONT_SIZE)  # Increase font size
        self.catalog_table.setFont(font)

        # Resize columns
        self.catalog_table.resizeColumnsToContents()
        table_header = self.catalog_table.horizontalHeader()
        if table_header is not None:
            table_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.catalog_table.setColumnWidth(0, 10)
