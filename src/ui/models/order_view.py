from src.backend.models.order import Order, has_analogs
from src.ui.models.column import TableColumn
from src.ui.models.view_model import ViewModel

headers = [
    TableColumn("Год", edit=True),
    TableColumn("Квартал", edit=True),
    TableColumn("Руководитель", edit=True),
    TableColumn("Сотрудник", edit=True),
    TableColumn("Наименование ПО", edit=True),
    TableColumn("Производитель ПО", edit=False),
    TableColumn("Тарифный план", edit=True),
    TableColumn("Логин и пароль", edit=True),
    TableColumn("Страна производства", edit=False),
    TableColumn("Количество", edit=True),
    TableColumn("Продление/новая", edit=True),
    TableColumn("Цена за единицу", edit=True),
    TableColumn("Стоимость", edit=False),
    TableColumn("Срока действия лицензии", edit=True),
    TableColumn("Тип лицензии", edit=True),
    TableColumn("Срок полезного использования", edit=True),
    TableColumn("Тип ПО", edit=False),
    TableColumn("Наличие в реестре", edit=True),
    TableColumn("Наличие аналогов", edit=True),
    TableColumn("Проект", edit=True),
    TableColumn("Ссылка", edit=False),
    TableColumn("Альтернативы", edit=False),
]


class OrderView(ViewModel):
    def __init__(
        self,
        order: Order,
        year: int,
        quarter: int,
        supervisor_name: str,
        employee_name: str,
        software_name: str,
        software_manufacturer: str,
        tariff_plan: str,
        login_and_password: str,
        country: str,
        number_license: int,
        is_new_license: str,
        price_for_one: float,
        total_price: float,
        licenses_period: str,
        license_type: str,
        useful_life: str,
        software_class: str,
        is_registered: str,
        is_analog_in_registry: str,
        project: str,
        link: str,
        alternatives: str,
    ):
        self.order = order
        self.year = year
        self.quarter = quarter
        self.supervisor_name = supervisor_name
        self.employee_name = employee_name
        self.software_name = software_name
        self.software_manufacturer = software_manufacturer
        self.tariff_plan = tariff_plan
        self.login_and_password = login_and_password
        self.country = country
        self.number_license = number_license
        self.is_new_license = is_new_license
        self.price_for_one = price_for_one
        self.total_price = total_price
        self.licenses_period = licenses_period
        self.license_type = license_type
        self.useful_life = useful_life
        self.software_class = software_class
        self.is_registered = is_registered
        self.is_analog_in_registry = is_analog_in_registry
        self.project = project
        self.link = link
        self.alternatives = alternatives

    def get_key(self) -> tuple:
        return (
            self.year,
            self.quarter,
            self.supervisor_name,
            self.employee_name,
            self.software_name,
            self.tariff_plan,
            self.login_and_password,
            self.country,
            self.licenses_period,
            self.license_type,
            self.useful_life,
            self.is_new_license,
            self.is_registered,
            self.is_analog_in_registry,
            self.project,
            self.link,
            self.alternatives,
        )

    @staticmethod
    def get_headers() -> list:
        return headers

    def to_array(self) -> list:
        return [
            self.year,
            self.quarter,
            self.supervisor_name,
            self.employee_name,
            self.software_name,
            self.software_manufacturer,
            self.tariff_plan,
            self.login_and_password,
            self.country,
            self.number_license,
            self.is_new_license,
            self.price_for_one,
            self.total_price,
            self.licenses_period,
            self.license_type,
            self.useful_life,
            self.software_class,
            self.is_registered,
            self.is_analog_in_registry,
            self.project,
            self.link,
            self.alternatives,
        ]

    @staticmethod
    def from_order(order: Order) -> "OrderView":
        return OrderView(
            order=order,
            year=order.year,
            quarter=order.quarter.number,
            supervisor_name=order.supervisor.name,
            employee_name=order.employee_name,
            software_name=order.software.name,
            software_manufacturer=order.software.maker_name if order.software.maker_name is not None else "",
            tariff_plan=order.tariff_plan if order.tariff_plan is not None else "",
            login_and_password=order.login_and_password if order.login_and_password is not None else "",
            country=order.software.country if isinstance(order.software.country, str) else order.software.country.name,
            number_license=order.number_license,
            is_new_license="Новая" if order.is_new_license else "Продление",
            price_for_one=order.price_for_one,
            total_price=order.price_for_one * order.number_license,
            licenses_period=order.licenses_period.isoformat() if order.licenses_period is not None else "",
            license_type=order.license_type.name,
            useful_life=order.useful_life,
            software_class=order.software.software_class if isinstance(order.software.software_class, str) else order.software.software_class.class_name,
            is_registered="Да" if order.software.is_in_registry else "Нет",
            is_analog_in_registry="Да" if has_analogs(order.software.software_analogs) else "Нет",
            project=order.company_which_will_use.name,
            link=order.software.website if order.software.website is not None else "",
            alternatives=order.software.software_analogs if order.software.software_analogs is not None else "",
        )
