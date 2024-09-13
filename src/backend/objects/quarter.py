from typing import ClassVar


class Quarter:
    _quarter_map: ClassVar[dict[str, int]] = {"1 квартал": 1, "2 квартал": 2, "3 квартал": 3, "4 квартал": 4}

    def __init__(self, name: str):
        self.name = name
        self.number = self._get_number_from_name(name)

    def __eq__(self, other):
        return self.name == other.name and self.number == other.number

    @classmethod
    def _get_number_from_name(cls, name: str) -> int:
        """
        Get the quarter number based on the quarter name.

        :param name: The name of the quarter.
        :return: The corresponding number of the quarter.
        :raises ValueError: If the name is not a valid quarter.
        """
        number = cls._quarter_map.get(name.lower())
        if number is None:
            error_message = f"Invalid quarter name: {name}"
            raise ValueError(error_message)
        return number
