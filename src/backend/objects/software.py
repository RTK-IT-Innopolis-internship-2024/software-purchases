from src.backend.objects.country import Country
from src.backend.objects.software_class import SoftwareClass


class Software:
    def __init__(
        self,
        country: Country,
        company: str | None,
        software_class: SoftwareClass,
        name: str,
        maker_name: str | None,
        website: str | None,
        purpose: str | None,
        software_analogs: str | None,
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

    def __eq__(self, other):
        return all(
            [
                self.country == other.country,
                self.software_class == other.software_class,
                self.name == other.name,
                self.maker_name == other.maker_name,
                self.website == other.website,
                self.purpose == other.purpose,
                self.software_analogs == other.software_analogs,
                self.company == other.company,
                self.registry_link == other.registry_link,
                self.is_in_registry == other.is_in_registry,
            ]
        )
