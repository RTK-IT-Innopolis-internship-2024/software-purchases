from datetime import date
from pathlib import Path

from src.backend.models.order_template import OrderTemplate
from src.ui.models.order_view import OrderView
from src.utils import utils


class OrderTemplateView:
    def __init__(self, order_template: OrderTemplate, file_path: str, orders: list[OrderView]):
        self.order_template = order_template
        self.file_path = file_path
        self.orders = orders

    def orders_in_period(self, start_date: date, end_date: date) -> list[OrderView]:
        result_orders = []
        start_year_quarter = utils.date_to_year_quarter(start_date)
        end_year_quarter = utils.date_to_year_quarter(end_date)
        for order in self.orders:
            year_quarter = (order.year, order.quarter)
            if start_year_quarter <= year_quarter <= end_year_quarter:
                result_orders.append(order)

        return result_orders

    def get_file_name(self) -> str:
        return Path(self.file_path).name

    def to_array_in_period(self, start_date: date, end_date: date) -> list:
        return [order.to_array() for order in self.orders_in_period(start_date, end_date)]

    def to_array(self) -> list:
        return [order.to_array() for order in self.orders]

    def to_dict(self) -> dict:
        return {self.file_path: [order.to_array() for order in self.orders]}

    @staticmethod
    def from_order_template(order_template: OrderTemplate) -> "OrderTemplateView":
        return OrderTemplateView(
            order_template=order_template,
            file_path=order_template.file_path,
            orders=[OrderView.from_order(order) for order in order_template.order_list] if order_template.order_list else [],
        )
