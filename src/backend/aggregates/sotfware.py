from eventsourcing.domain import Aggregate


class Software(Aggregate):
    """
    Represents the 'SoftwareClass' aggregate.
    """

    class Registered(Aggregate.Created):
        """
        Event triggered when a software class is registered.
        """

        software_class_id: str
