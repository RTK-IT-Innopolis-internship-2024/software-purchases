from datetime import date

from src.backend.objects.company import Company
from src.backend.objects.license_type import LicenseType
from src.backend.objects.software import Software
from src.backend.objects.supervisor import Supervisor


class Order:
    def __init__(
        self,
        year: int,
        quarter: int,
        supervisor: Supervisor,
        software: Software,
        employee_name: str,
        tariff_plan: str,
        login_and_password: str | None,
        number_license: int,
        price_for_one: float,
        licenses_period: date | None,
        license_type: LicenseType,
        useful_life: str,
        company_which_will_use: Company,
        is_new_license: bool,
        is_registered: bool,
        is_analog_in_registry: bool,
    ):
        self.year = year
        self.quarter = quarter
        self.supervisor = supervisor
        self.software = software
        self.employee_name = employee_name
        self.tariff_plan = tariff_plan
        self.login_and_password = login_and_password
        self.number_license = number_license
        self.is_new_license = is_new_license
        self.price_for_one = price_for_one
        self.licenses_period = licenses_period
        self.license_type = license_type
        self.useful_life = useful_life
        self.is_registered = is_registered
        self.is_analog_in_registry = is_analog_in_registry
        self.company_which_will_use = company_which_will_use
