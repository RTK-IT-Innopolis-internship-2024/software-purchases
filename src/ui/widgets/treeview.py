from PyQt6.QtWidgets import QTreeView


class TreeView(QTreeView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setColumnWidth(0, 100)
        self.setFixedWidth(300)

    def load_model(self, model) -> None:
        self.setModel(model)

    def clear_view(self) -> None:
        self.destroy(destroySubWindows=True)
