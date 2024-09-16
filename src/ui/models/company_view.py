from src.backend.objects.company import Company
from src.ui.models.column import TableColumn
from src.ui.models.view_model import ViewModel

company_headers = [
    TableColumn("Название компании", edit=False),
]


class CompanyView(ViewModel):
    def __init__(self, company: Company, name: str):
        self.company = company
        self.name = name

    @staticmethod
    def get_headers() -> list:
        return company_headers

    def to_array(self) -> list:
        return [self.name]

    @staticmethod
    def from_company(company: Company) -> "CompanyView":
        return CompanyView(company=company, name=company.name)
