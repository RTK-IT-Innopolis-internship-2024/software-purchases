from datetime import UTC, datetime
from typing import TYPE_CHECKING

from src import app
from src.backend.controllers import order_template_controller
from src.backend.controllers.final_reports_controller import create_orders_report_with_sort_by_params

if TYPE_CHECKING:
    from src.backend.objects.order import Order


def test() -> None:
    # example code to show how to use backend in ui
    dt_start = datetime.strptime("2024-08-20", "%Y-%m-%d").replace(tzinfo=UTC).date()
    dt_end = datetime.strptime("2024-10-20", "%Y-%m-%d").replace(tzinfo=UTC).date()

    order_templates_by_period = order_template_controller.get_order_templates_by_period(dt_start, dt_end)

    sort_params = {"supervisor.name": True, "software.name": True, "tariff_plan": False, "is_new_license": True}

    order_list: list[Order] | None = order_templates_by_period[0].order_list

    create_orders_report_with_sort_by_params(dt_start, dt_end, order_list, sort_params)


if __name__ == "__main__":
    # test()

    # your code
    app.run()
