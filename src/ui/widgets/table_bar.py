import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QPushButton, QDateEdit, QSpacerItem, QSizePolicy
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon

class TableBar(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        # Period label
        self.period_label = QLabel("Период:")
        self.period_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-right: 10px;")
        layout.addWidget(self.period_label)

        # DateEdit "From" selector
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate())
        self.date_from.setStyleSheet("font-size: 14px; padding: 5px;")
        self.date_from.setFixedHeight(30)
        layout.addWidget(self.date_from)

        self.dash_label = QLabel("-")
        self.dash_label.setStyleSheet("font-size: 16px; margin-left: 2px; margin-right: 2px;")
        layout.addWidget(self.dash_label)

        # DateEdit "To" selector
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setStyleSheet("font-size: 14px; padding: 5px;")
        self.date_to.setFixedHeight(30)
        layout.addWidget(self.date_to)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addSpacerItem(spacer)

        # Button with icon "+"
        self.add_button = QPushButton()
        self.add_button.setIcon(QIcon.fromTheme("list-add"))
        #self.add_button.setStyleSheet("color: #4CAF50;")
        layout.addWidget(self.add_button)

        self.setLayout(layout)