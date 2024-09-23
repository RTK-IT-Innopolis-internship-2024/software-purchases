import sys
from pathlib import Path


class AppConfig:
    """
    Configuration File
    """

    APP_NAME: str = "БФТ Закупки"

    PROJECT_ROOT: Path = Path(sys.argv[0]).resolve().parent
    FONT_SIZE: int = 12

    @classmethod
    def initialize(cls) -> None:
        """
        Perform any necessary initializations here, e.g.:
        - Loading settings from a file
        """
        # Create orders/order_templates and orders/main_template if they don't exist
        order_templates_path = Path(cls.get_order_path("orders/order_templates"))
        order_templates_path.mkdir(parents=True, exist_ok=True)

        main_order_template_path = Path(cls.get_order_path("orders/main_template"))
        main_order_template_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_order_path(cls, relative_path: str) -> str:
        """
        Returns the absolute path to a resource, useful for handling files in PyInstaller-built applications.

        :param relative_path: Relative path to the resource.
        :return: Absolute path to the resource.
        """
        return str(cls.PROJECT_ROOT / relative_path)

    @classmethod
    def get_resource_path(cls, relative_path: str) -> str:
        """
        Returns the absolute path to a resource, useful for handling files in PyInstaller-built applications.

        :param relative_path: Relative path to the resource.
        :return: Absolute path to the resource.
        """
        base_path = Path(getattr(sys, "_MEIPASS", cls.PROJECT_ROOT))

        return str(base_path / relative_path)
