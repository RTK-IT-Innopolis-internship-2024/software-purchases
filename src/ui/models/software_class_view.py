from src.backend.models.software_class import SoftwareClass
from src.ui.models.column import TableColumn
from src.ui.models.view_model import ViewModel

software_class_headers = [
    TableColumn("Секция класса", edit=False),
    TableColumn("Код класса", edit=True),
    TableColumn("Название класса", edit=False),
    TableColumn("Индикатор текущего года (первая половина)", edit=True, width=150, height_multiplier=2.2),
    TableColumn("Индикатор текущего года (вторая половина)", edit=True, width=150, height_multiplier=2.2),
    TableColumn("Индикатор следующего года (первая половина)", edit=True, width=150, height_multiplier=2.2),
    TableColumn("Индикатор следующего года (вторая половина)", edit=True, width=150, height_multiplier=2.2),
]


class SoftwareClassView(ViewModel):
    def __init__(
        self,
        software_class: SoftwareClass,
        class_section: str,
        class_point: str,
        class_name: str,
        target_indicator_current_year_first_half: str | float,
        target_indicator_current_year_second_half: str | float,
        target_indicator_next_year_first_half: str | float,
        target_indicator_next_year_second_half: str | float,
    ):
        self.software_class = software_class
        self.class_section = class_section
        self.class_point = class_point
        self.class_name = class_name
        self.target_indicator_current_year_first_half = target_indicator_current_year_first_half
        self.target_indicator_current_year_second_half = target_indicator_current_year_second_half
        self.target_indicator_next_year_first_half = target_indicator_next_year_first_half
        self.target_indicator_next_year_second_half = target_indicator_next_year_second_half

    @staticmethod
    def get_headers() -> list:
        return software_class_headers

    def to_array(self) -> list:
        return [
            self.class_section,
            self.class_point,
            self.class_name,
            self.target_indicator_current_year_first_half,
            self.target_indicator_current_year_second_half,
            self.target_indicator_next_year_first_half,
            self.target_indicator_next_year_second_half,
        ]

    @staticmethod
    def from_software_class(software_class: SoftwareClass) -> "SoftwareClassView":
        return SoftwareClassView(
            software_class=software_class,
            class_section=software_class.class_section.name,
            class_point=software_class.class_point if software_class.class_point else "",
            class_name=software_class.class_name,
            target_indicator_current_year_first_half=software_class.target_indicator_current_year_first_half
            if software_class.target_indicator_current_year_first_half is not None
            else "",
            target_indicator_current_year_second_half=software_class.target_indicator_current_year_second_half
            if software_class.target_indicator_current_year_second_half is not None
            else "",
            target_indicator_next_year_first_half=software_class.target_indicator_next_year_first_half
            if software_class.target_indicator_next_year_first_half is not None
            else "",
            target_indicator_next_year_second_half=software_class.target_indicator_next_year_second_half
            if software_class.target_indicator_next_year_second_half is not None
            else "",
        )
