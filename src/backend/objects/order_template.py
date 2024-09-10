from src.backend.objects.company import Company
from src.backend.objects.country import Country
from src.backend.objects.license_type import LicenseType
from src.backend.objects.order import Order
from src.backend.objects.software import Software
from src.backend.objects.software_class import SoftwareClass
from src.backend.objects.supervisor import Supervisor


class OrderTemplate:
    def __init__(
        self,
        file_path: str,
        companies: list[Company],
        countries: list[Country],
        supervisors: list[Supervisor],
        license_type: list[LicenseType],
        software_classes: list[SoftwareClass],
        software_list: list[Software],
        order_list: list[Order] | None,
    ):
        self.file_path = file_path
        self.companies = companies
        self.countries = countries
        self.supervisors = supervisors
        self.license_type = license_type
        self.software_classes = software_classes
        self.software_list = software_list
        self.order_list = order_list
