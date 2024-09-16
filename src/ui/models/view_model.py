from abc import ABC, abstractmethod

from src.ui.models.column import TableColumn


class ViewModel(ABC):
    @staticmethod
    @abstractmethod
    def get_headers() -> list[TableColumn]:
        raise NotImplementedError

    @abstractmethod
    def to_array(self) -> list:
        raise NotImplementedError
