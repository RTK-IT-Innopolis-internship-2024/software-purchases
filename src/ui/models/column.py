class TableColumn:
    def __init__(self, name: str, width: int | None = None, height_multiplier: float = 1, *, edit: bool = True):
        self.name = name
        self.edit = edit
        self.width = width
        self.height_multiplier = height_multiplier
