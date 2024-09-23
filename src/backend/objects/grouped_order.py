from datetime import date

from src.backend.objects.company import Company
from src.backend.objects.license_type import LicenseType
from src.backend.objects.software import Software
from src.backend.objects.supervisor import Supervisor


class GroupedOrder:
    def __init__(
        self,
        software: Software,
        supervisor: Supervisor,
        employee_names: str,
        company_which_will_use: Company,
        tariff_plan: str | None,
        login_and_password: str | None,
        number_orders: int,
        number_license: int,
        price_for_one: float,
        licenses_period: date | None,
        license_type: LicenseType,
        useful_life: str,
        is_new_license: bool,
    ):
        self.supervisor = supervisor
        self.employee_names = employee_names
        self.software = software
        self.tariff_plan = tariff_plan
        self.login_and_password = login_and_password
        self.number_orders = number_orders
        self.number_license = number_license
        self.is_new_license = is_new_license
        self.price_for_one = price_for_one
        self.licenses_period = licenses_period
        self.license_type = license_type
        self.useful_life = useful_life
        self.company_which_will_use = company_which_will_use
