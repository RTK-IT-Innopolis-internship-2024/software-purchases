from uuid import UUID

from eventsourcing.application import Application

from src.backend.aggregates.order_template_aggregate import OrderTemplateAggregate
from src.backend.objects.order_template import OrderTemplate


class OrderTemplateHandler(Application):
    def register_order_template(self, order_template: OrderTemplate) -> UUID:
        reps_order_template = OrderTemplateAggregate(order_template)
        self.save(reps_order_template)
        return reps_order_template.id

    def get_order_template(self, order_template_id: UUID):
        return self.repository.get(order_template_id)
