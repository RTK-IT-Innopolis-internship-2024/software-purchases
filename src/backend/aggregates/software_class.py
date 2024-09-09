from eventsourcing.domain import Aggregate, event


class SoftwareClass(Aggregate):
    """
    Represents the 'SoftwareClass' aggregate.
    """

    class Registered(Aggregate.Created):
        """
        Event triggered when a software class is registered.
        """

        software_class_number: str
        software_type: str
        target_value_description: str

    @event(Registered)
    def __init__(self, software_class_number: str, software_type: str, target_value_description: str = ""):
        """
        Initializes a SoftwareClass object with the given details.

        :param software_class_number: The number of the software class.
        :param software_type: The type of the software.
        :param target_value_description: Description of the target value (optional).
        """
        self.software_class_number = software_class_number
        self.software_type = software_type
        self.target_value_description = target_value_description

    def edit(self, **kwargs):
        """
        Public method to edit specific attributes of the software class.

        :param kwargs: Key-value pairs of attributes to be updated.
        """
        # Define a list of allowed fields for editing
        allowed_fields = ["software_class_number", "software_type", "target_value_description"]

        # Determine changes only for allowed fields with valid values
        changes = {
            k: v
            for k, v in kwargs.items()
            if k in allowed_fields  # The key must be in the list of allowed fields
            and v is not None  # The value must not be None
            and hasattr(self, k)  # The attribute must exist in the object
            and getattr(self, k) != v  # The current value must be different
        }

        # Call the private method only if there are valid changes
        if changes:
            self._edit(**changes)

    class SoftwareClassEdited(Aggregate.Event):
        """
        Event triggered when a software class details are edited.
        """

    @event(SoftwareClassEdited)
    def _edit(self, **kwargs):
        """
        Private method to apply the changes to the software class.

        :param kwargs: Key-value pairs of attributes to be updated.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)  # Dynamically set the attribute
