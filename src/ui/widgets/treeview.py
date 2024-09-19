from datetime import date
from pathlib import Path

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

    def on_item_changed(self, item, _):
        """Handle checkbox changes to dim/cross out text and propagate changes to children."""
        if item.checkState(0) == Qt.CheckState.Unchecked:
            font = item.font(0)
            font.setStrikeOut(True)
            item.setFont(0, font)
            item.setForeground(0, QBrush(Qt.GlobalColor.gray))
            # If a parent is unchecked, uncheck all children
            for i in range(item.childCount()):
                child = item.child(i)
                child.setCheckState(0, Qt.CheckState.Unchecked)
        else:
            font = item.font(0)
            font.setStrikeOut(False)
            item.setFont(0, font)
            item.setForeground(0, QBrush(Qt.GlobalColor.black))
            # If a parent is checked, check all children
            for i in range(item.childCount()):
                child = item.child(i)
                child.setCheckState(0, Qt.CheckState.Checked)

    def populate_tree(self, data: list[OrderTemplateView], period: tuple[date, date]):
        """Populates the tree with template files and their orders."""
        self.clear()  # Clear any existing items
        for template_view in data:
            # Create the top-level item (template file)
            top_item = QTreeWidgetItem(self)
            file_name = Path(template_view.file_path).name
            top_item.setText(0, file_name)
            top_item.setCheckState(0, Qt.CheckState.Checked)
            font = QFont("", weight=QFont.Weight.Bold)
            font.setPointSize(AppConfig.FONT_SIZE)
            top_item.setFont(0, font)
            self.addTopLevelItem(top_item)

            # Add orders as child items under each template
            for order in template_view.orders_in_period(period[0], period[1]):
                child_item = QTreeWidgetItem(top_item)
                child_item.setText(0, f"Заявка: {order.employee_name}")  # Customize the display for each order
                child_item.setCheckState(0, Qt.CheckState.Checked)
                child_item.setFont(0, font)
                top_item.addChild(child_item)
