from datetime import UTC, datetime

from src import app
from src.backend.controllers import order_template_controller

if __name__ == "__main__":
    # example code to show how to use backend in ui
    main_order_template = order_template_controller.get_main_order_template()

    dt_start = datetime.strptime("2024-08-20", "%Y-%m-%d").replace(tzinfo=UTC)
    dt_end = datetime.strptime("2024-10-20", "%Y-%m-%d").replace(tzinfo=UTC)

    order_templates_by_period = order_template_controller.get_order_templates_by_period(dt_start, dt_end)

    # your code
    app.run()
