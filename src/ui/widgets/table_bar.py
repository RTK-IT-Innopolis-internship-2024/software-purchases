import typing
from datetime import UTC, date, datetime

from src.utils.utils import date_to_year_quarter, quarter_to_date_range

if typing.TYPE_CHECKING:
    from collections.abc import Callable

from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDateEdit, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QWidget


class TableBar(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout()
        self.on_period_changed: Callable[[QDate, QDate], None] = lambda *_: None
        self.on_refresh_document: Callable[[], None] = lambda: None

        # Period label
        self.period_label = QLabel("Период:")
        self.period_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-right: 10px;")
        layout.addWidget(self.period_label)

        year, quarter = date_to_year_quarter(datetime.now(tz=UTC).date())
        start_date, end_date = quarter_to_date_range(year, quarter)
        # DateEdit "From" selector
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(start_date)
        self.date_from.setStyleSheet("font-size: 14px; padding: 5px;")
        self.date_from.setFixedHeight(30)
        self.date_from.dateChanged.connect(self.__on_period_changed)
        layout.addWidget(self.date_from)

        self.dash_label = QLabel("-")
        self.dash_label.setStyleSheet("font-size: 16px; margin-left: 2px; margin-right: 2px;")
        layout.addWidget(self.dash_label)

        # DateEdit "To" selector
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(end_date)
        self.date_to.setStyleSheet("font-size: 14px; padding: 5px;")
        self.date_to.setFixedHeight(30)
        self.date_to.dateChanged.connect(self.__on_period_changed)
        layout.addWidget(self.date_to)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addSpacerItem(spacer)

        # Button with icon "refresh"
        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(QIcon.fromTheme("view-refresh"))
        layout.addWidget(self.refresh_button)
        self.refresh_button.clicked.connect(self.refresh_document)

        self.setLayout(layout)

    def refresh_document(self) -> None:
        self.on_refresh_document()

    def __on_period_changed(self) -> None:
        self.on_period_changed(
            self.date_from.date(),
            self.date_to.date(),
        )

    def get_period(self) -> tuple[QDate, QDate]:
        return self.date_from.date(), self.date_to.date()

    def get_period_dates(self) -> tuple[date, date]:
        return self.date_from.date().toPyDate(), self.date_to.date().toPyDate()
