class TableColumn:
    def __init__(self, name: str, edit: bool = True, width: int | None = None, height_multiplier: float = 1):
        self.name = name
        self.edit = edit
        self.width = width
        self.height_multiplier = height_multiplier
