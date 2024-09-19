from datetime import date

from src.backend.objects.company import Company
from src.backend.objects.license_type import LicenseType
from src.backend.objects.quarter import Quarter
from src.backend.objects.software import Software
from src.backend.objects.supervisor import Supervisor


def has_analogs(software_analogs: str | None) -> bool:
    if software_analogs is None:
        return False
    return not (len(software_analogs) == 0 or software_analogs.lower() == "нет" or software_analogs.lower() == "не требуется")


class Order:
    def __init__(
        self,
        year: int,
        quarter: Quarter,
        software: Software,
        supervisor: Supervisor,
        company_which_will_use: Company,
        employee_name: str,
        tariff_plan: str | None,
        login_and_password: str | None,
        number_license: int,
        price_for_one: float,
        licenses_period: date | None,
        license_type: LicenseType,
        useful_life: str,
        is_new_license: bool,
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
        self.company_which_will_use = company_which_will_use

    def __eq__(self, other):
        return all(
            [
                self.year == other.year,
                self.quarter == other.quarter,
                self.supervisor == other.supervisor,
                self.software == other.software,
                self.employee_name == other.employee_name,
                self.tariff_plan == other.tariff_plan,
                self.login_and_password == other.login_and_password,
                self.number_license == other.number_license,
                self.is_new_license == other.is_new_license,
                self.price_for_one == other.price_for_one,
                self.licenses_period == other.licenses_period,
                self.license_type == other.license_type,
                self.useful_life == other.useful_life,
                self.company_which_will_use == other.company_which_will_use,
            ]
        )
