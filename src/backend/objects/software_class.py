from src.backend.objects.software_class_section import SoftwareClassSection


class SoftwareClass:
    def __init__(
        self,
        class_section: SoftwareClassSection,
        class_point: str | None,
        class_name: str,
        target_indicator_name: str | None,
        target_indicator_current_year_first_half: str | float | None,
        target_indicator_current_year_second_half: str | float | None,
        target_indicator_next_year_first_half: str | float | None,
        target_indicator_next_year_second_half: str | float | None,
    ):
        self.class_section = class_section
        self.class_point = class_point
        self.class_name = class_name
        self.target_indicator_name = target_indicator_name

        self.target_indicator_current_year_first_half = target_indicator_current_year_first_half
        self.target_indicator_current_year_second_half = target_indicator_current_year_second_half
        self.target_indicator_next_year_first_half = target_indicator_next_year_first_half
        self.target_indicator_next_year_second_half = target_indicator_next_year_second_half

    def __eq__(self, other):
        return all(
            [
                self.class_section == other.class_section,
                self.class_point == other.class_point,
                self.class_name == other.class_name,
                self.target_indicator_name == other.target_indicator_name,
                self.target_indicator_current_year_first_half == other.target_indicator_current_year_first_half,
                self.target_indicator_current_year_second_half == other.target_indicator_current_year_second_half,
                self.target_indicator_next_year_first_half == other.target_indicator_next_year_first_half,
                self.target_indicator_next_year_second_half == other.target_indicator_next_year_second_half,
            ]
        )
