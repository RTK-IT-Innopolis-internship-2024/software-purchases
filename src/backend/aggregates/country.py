from eventsourcing.domain import Aggregate, event


class Country(Aggregate):
    """
    Represents the 'Country' aggregate.
    """

    class Registered(Aggregate.Created):
        """
        Event triggered when a country is registered.
        """

        name: str

    @event(Registered)
    def __init__(self, name: str):
        """
        Initializes a Country object with the given name.

        :param name: The name of the country.
        """
        self.name = name

    def edit(self, name=None) -> bool:
        """
        Public method to change the name of the country.
        If a parameter is not provided, no changes are made.

        :param name: The new name of the country (optional).
        """
        if name is not None and name != self.name:
            self._edit(name=name)
            return True
        return False

    class CountryEdited(Aggregate.Event):
        """
        Event triggered when a country's name is edited.
        """

        name: str

    @event(CountryEdited)
    def _edit(self, name: str):
        """
        Private method to apply the name change of the country.

        :param name: The new name of the country.
        """
        self.name = name
