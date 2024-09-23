from src.backend.objects.software import Software
from src.ui.models.column import TableColumn
from src.ui.models.view_model import ViewModel

software_headers = [
    TableColumn("Название ПО", edit=True),
    TableColumn("Производитель ПО", edit=True),
    TableColumn("Страна", edit=True),
    TableColumn("Сайт", edit=True),
    TableColumn("Назначение", edit=True),
    TableColumn("Аналоги", edit=True),
    TableColumn("Ссылка на реестр", edit=True),
    TableColumn("Присутствие в реестре", edit=False, width=100, height_multiplier=2),
]


class SoftwareView(ViewModel):
    def __init__(
        self,
        software: Software,
        name: str,
        maker_name: str,
        country: str,
        website: str,
        purpose: str,
        software_analogs: str,
        registry_link: str,
        is_in_registry: str,
    ):
        self.software = software
        self.name = name
        self.maker_name = maker_name
        self.country = country
        self.website = website
        self.purpose = purpose
        self.software_analogs = software_analogs
        self.registry_link = registry_link
        self.is_in_registry = is_in_registry

    @staticmethod
    def get_headers() -> list:
        return software_headers

    def to_array(self) -> list:
        return [
            self.name,
            self.maker_name,
            self.country,
            self.website,
            self.purpose,
            self.software_analogs,
            self.registry_link,
            self.is_in_registry,
        ]

    @staticmethod
    def from_software(software: Software) -> "SoftwareView":
        return SoftwareView(
            software=software,
            name=software.name,
            maker_name=software.maker_name if software.maker_name else "",
            country=software.country.name,
            website=software.website if software.website else "",
            purpose=software.purpose if software.purpose else "",
            software_analogs=software.software_analogs if software.software_analogs else "",
            registry_link=software.registry_link if software.registry_link else "",
            is_in_registry="Да" if software.is_in_registry else "Нет",
        )
