from src.backend.objects.company import Company
from src.backend.objects.country import Country
from src.backend.objects.software_class import SoftwareClass


class Software:
    def __init__(
        self,
        country: Country,
        software_class: SoftwareClass,
        name: str,
        maker_name: str,
        website: str | None,
        purpose: str | None,
        software_analogs: str | None,
        company: Company | None,
        registry_link: str | None,
        *,
        is_in_registry: bool,
    ):
        self.name = name
        self.maker_name = maker_name
        self.country = country
        self.website = website
        self.purpose = purpose
        self.software_class = software_class
        self.software_analogs = software_analogs
        self.company = company
        self.is_in_registry = is_in_registry
        self.registry_link = registry_link
