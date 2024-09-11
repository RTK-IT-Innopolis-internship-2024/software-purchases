from src.backend.objects.order_template import OrderTemplate
from src.ui.models.order_view import OrderView


class OrderTemplateView:
    def __init__(self, order_template: OrderTemplate, file_path: str, orders: list[OrderView]):
        self.order_template = order_template
        self.file_path = file_path
        self.orders = orders

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
