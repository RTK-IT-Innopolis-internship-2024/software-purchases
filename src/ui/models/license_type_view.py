from src.backend.models.license_type import LicenseType
from src.ui.models.column import TableColumn
from src.ui.models.view_model import ViewModel

license_type_headers = [
    TableColumn("Тип лицензии", edit=False),
]


class LicenseTypeView(ViewModel):
    def __init__(self, license_type: LicenseType, name: str):
        self.license_type = license_type
        self.name = name

    @staticmethod
    def get_headers() -> list:
        return license_type_headers

    def to_array(self) -> list:
        return [self.name]

    @staticmethod
    def from_license_type(license_type: LicenseType) -> "LicenseTypeView":
        return LicenseTypeView(license_type=license_type, name=license_type.name)
