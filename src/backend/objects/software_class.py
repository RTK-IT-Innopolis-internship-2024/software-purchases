class SoftwareClass:
    def __init__(self, class_point: str, class_name: str, target_indicator_name: str, target_indicator_value: float | None = None):
        self.class_point = class_point
        self.class_name = class_name
        self.target_indicator_name = target_indicator_name
        self.target_indicator_value = target_indicator_value

    def __str__(self):
        return f"{self.class_point} {self.class_name}"
