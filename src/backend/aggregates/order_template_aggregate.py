from eventsourcing.domain import Aggregate, event

from src.backend.objects.order_template import OrderTemplate


class OrderTemplateAggregate(Aggregate):
    class Registered(Aggregate.Created):
        order_template: OrderTemplate

    @event(Registered)
    def __init__(self, order_template: OrderTemplate):
        self.order_template = order_template
