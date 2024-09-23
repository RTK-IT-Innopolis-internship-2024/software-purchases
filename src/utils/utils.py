import calendar
from datetime import date, datetime
from pathlib import Path
from typing import Any


def deep_print(current_obj: Any, max_depth: int = 3, name: str = "init", current_level: int = 0) -> None:
    if current_level > max_depth:
        return
    standard_types = [str, int, float, bool, list, dict, type(None), datetime, date, Path]
    str_content = ""
    # if not list, dict and has override __str__ or __repr__
    if not isinstance(current_obj, list) and not isinstance(current_obj, dict):
        str_content = str(current_obj)
    print(f"{'  ' * current_level} {name} [{type(current_obj)}]: {str_content}")  # noqa: T201
    if isinstance(current_obj, list):
        for i, o in enumerate(current_obj):
            deep_print(o, max_depth, str(i), current_level + 1)
    elif isinstance(current_obj, dict):
        for k, v in current_obj.items():
            deep_print(v, max_depth, str(k), current_level + 1)
    else:
        if type(current_obj) in standard_types:
            return
        for o in dir(current_obj):
            if not o.startswith("_"):
                deep_print(getattr(current_obj, o), max_depth, o, current_level + 1)


def date_to_year_quarter(date: date) -> tuple[int, int]:
    """
    Function to convert date to tuple of year and quarter.

    Args:
    ----
        date (date): Date to convert.

    Returns:
    -------
          tuple: Tuple of year and quarter.

    """
    return (date.year, (date.month - 1) // 3 + 1)


def quarter_to_date_range(year: int, quarter: int) -> tuple[date, date]:
    """
    Function to convert year and quarter to tuple of date range.

    Args:
    ----
        year (int): Year to convert.
        quarter (int): Quarter to convert.

    Returns:
    -------
          tuple: Tuple of date range.

    """
    return (
        date(year, (quarter - 1) * 3 + 1, 1),
        date(year, quarter * 3, calendar.monthrange(year, quarter * 3)[1]),
    )
