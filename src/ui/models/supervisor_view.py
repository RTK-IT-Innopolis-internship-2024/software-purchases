from src.backend.models.supervisor import Supervisor
from src.ui.models.column import TableColumn
from src.ui.models.view_model import ViewModel

supervisor_headers = [
    TableColumn("Имя руководителя", edit=True),
    TableColumn("Email руководителя", edit=True),
]


class SupervisorView(ViewModel):
    def __init__(self, supervisor: Supervisor, name: str, email: str):
        self.supervisor = supervisor
        self.name = name
        self.email = email

    @staticmethod
    def get_headers() -> list:
        return supervisor_headers

    def to_array(self) -> list:
        return [self.name, self.email]

    @staticmethod
    def from_supervisor(supervisor: Supervisor) -> "SupervisorView":
        return SupervisorView(supervisor=supervisor, name=supervisor.name, email=supervisor.email if supervisor.email else "")
