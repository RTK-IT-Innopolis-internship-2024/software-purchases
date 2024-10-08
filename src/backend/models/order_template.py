from src.backend.models.company import Company
from src.backend.models.country import Country
from src.backend.models.license_type import LicenseType
from src.backend.models.order import Order
from src.backend.models.software import Software
from src.backend.models.software_class import SoftwareClass
from src.backend.models.supervisor import Supervisor


class OrderTemplate:
    def __init__(
        self,
        file_path: str,
        companies: list[Company],
        countries: list[Country],
        supervisors: list[Supervisor],
        license_types: list[LicenseType],
        software_classes: list[SoftwareClass],
        software_list: list[Software],
        order_list: list[Order] | None,
    ):
        self.file_path = file_path
        self.companies = companies
        self.countries = countries
        self.supervisors = supervisors
        self.license_type = license_types
        self.software_classes = software_classes
        self.software_list = software_list
        self.order_list = order_list

    def __eq__(self, other):
        return all(
            [
                self.file_path == other.file_path,
                self.companies == other.companies,
                self.countries == other.countries,
                self.supervisors == other.supervisors,
                self.license_type == other.license_type,
                self.software_classes == other.software_classes,
                self.software_list == other.software_list,
                self.order_list == other.order_list,
            ]
        )
