import typing
from datetime import date

if typing.TYPE_CHECKING:
    from collections.abc import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QFont
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem

from src.ui.models.order_template_view import OrderTemplateView
from src.utils.config import AppConfig


class TreeView(QTreeWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setHeaderHidden(True)  # We don't need a header
        self.itemChanged.connect(self.on_item_changed)
        self.itemExpanded.connect(self.update_persistant_state)
        self.itemCollapsed.connect(self.update_persistant_state)
        self.on_state_changed: Callable[[dict], None] = lambda *_: None
        self.initialized = False
        self.persistant_state: dict = {}
        self.current_state: dict = {}

    def update_font(self, item: QTreeWidgetItem):
        """Updates the font of an item."""
        if item.checkState(0) == Qt.CheckState.Unchecked:
            font = item.font(0)
            font.setStrikeOut(True)
            item.setFont(0, font)
            item.setForeground(0, QBrush(Qt.GlobalColor.gray))
        else:
            font = item.font(0)
            font.setStrikeOut(False)
            item.setFont(0, font)
            item.setForeground(0, QBrush(Qt.GlobalColor.black))

    def on_item_changed(self, item, _) -> None:
        """Handle checkbox changes to dim/cross out text and propagate changes to children."""
        if not self.initialized:
            return

        self.update_font(item)
        for i in range(item.childCount()):
            child = item.child(i)
            child.setCheckState(0, item.checkState(0))

        self.update_persistant_state()

        self.on_state_changed(self.current_state)

    def update_persistant_state(self) -> None:
        """Updates the persistant state of the tree."""
        if not self.initialized:
            return

        for top_key, data in self.persistant_state.items():
            data["checked"] = data["item"].checkState(0)
            data["expanded"] = data["item"].isExpanded()
            if top_key in self.current_state:
                self.current_state[top_key]["checked"] = data["checked"] == Qt.CheckState.Checked
            for key, order in data["orders"].items():
                order["checked"] = order["item"].checkState(0)
                if top_key in self.current_state and key in self.current_state[top_key]["orders"]:
                    self.current_state[top_key]["orders"][key]["checked"] = order["checked"] == Qt.CheckState.Checked

    def populate_tree(self, data: list[OrderTemplateView], period: tuple[date, date]) -> None:
        """Populates the tree with template files and their orders."""
        self.initialized = False
        self.clear()  # Clear any existing items
        self.current_state = {}
        for template_view in data:
            orders = template_view.orders_in_period(period[0], period[1])
            if len(orders) == 0:
                continue
            # Create the top-level item (template file)
            top_item = QTreeWidgetItem(self)
            file_name = template_view.get_file_name()
            top_item.setText(0, file_name)
            if file_name in self.persistant_state:
                top_item.setCheckState(0, self.persistant_state[file_name]["checked"])
                top_item.setExpanded(self.persistant_state[file_name]["expanded"])
                self.persistant_state[file_name]["item"] = top_item
            else:
                top_item.setCheckState(0, Qt.CheckState.Checked)
                self.persistant_state[file_name] = {"checked": Qt.CheckState.Checked, "expanded": False, "item": top_item, "orders": {}}

            self.current_state[file_name] = {"checked": top_item.checkState(0) == Qt.CheckState.Checked, "orders": {}}
            font = QFont("Arial", weight=QFont.Weight.Bold)
            font.setPointSize(AppConfig.FONT_SIZE)
            top_item.setFont(0, font)
            self.update_font(top_item)
            self.addTopLevelItem(top_item)

            # Add orders as child items under each template
            for order in orders:
                child_item = QTreeWidgetItem(top_item)
                child_item.setText(0, f"{order.employee_name}: {order.software_name}")  # Customize the display for each order
                key = order.get_key()
                if key in self.persistant_state[file_name]["orders"]:
                    child_item.setCheckState(0, self.persistant_state[file_name]["orders"][key]["checked"])
                    self.persistant_state[file_name]["orders"][key]["item"] = child_item
                else:
                    child_item.setCheckState(0, Qt.CheckState.Checked)
                    self.persistant_state[file_name]["orders"][key] = {"checked": Qt.CheckState.Checked, "item": child_item}

                self.current_state[file_name]["orders"][key] = {"checked": child_item.checkState(0) == Qt.CheckState.Checked}
                child_item.setFont(0, font)
                self.update_font(child_item)
                top_item.addChild(child_item)

        self.initialized = True
