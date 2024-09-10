import sys
from pathlib import Path


class AppConfig:
    """
    Configuration File
    """

    APP_NAME: str = "БФТ Закупки"

    BASE_PATH: Path = Path(__file__).resolve().parent
    PROJECT_ROOT: Path = Path(sys.argv[0]).resolve().parent

    @classmethod
    def initialize(cls) -> None:
        """
        Perform any necessary initializations here, e.g.:
        - Loading settings from a file
        """

    @classmethod
    def get_resource_path(cls, relative_path: str) -> str:
        """
        Returns the absolute path to a resource, useful for handling files in PyInstaller-built applications.

        :param relative_path: Relative path to the resource.
        :return: Absolute path to the resource.
        """
        return str(cls.PROJECT_ROOT / relative_path)
