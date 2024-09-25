from src.backend.models.country import Country
from src.ui.models.column import TableColumn
from src.ui.models.view_model import ViewModel

country_headers = [
    TableColumn("Название страны", edit=False),
]


class CountryView(ViewModel):
    def __init__(self, country: Country, name: str):
        self.country = country
        self.name = name

    @staticmethod
    def get_headers() -> list:
        return country_headers

    def to_array(self) -> list:
        return [self.name]

    @staticmethod
    def from_country(country: Country) -> "CountryView":
        return CountryView(country=country, name=country.name)
