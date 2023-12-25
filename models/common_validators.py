import datetime
import re
from typing import Optional


def common_id_validator(id: int | None, nullable: bool = False):
    if nullable and id is None:
        return id
    if not (isinstance(id, int) and id > 0):
        raise ValueError("ID has to be an integer greater than zero")
    return id


def common_string_validator(value: str | None,
                            min_length: int,
                            max_length: int,
                            nullable: bool = False,
                            alnum: bool = False,
                            pattern: Optional[re.Pattern] = None):
    if nullable and value is None:
        return value
    if not nullable and not value:
        raise ValueError("Value cannot be empty")
    if not min_length <= len(value) <= max_length:
        raise ValueError(f"Value has to have between {min_length} and {max_length} characters")
    if alnum and not value.isalnum():
        raise ValueError("Value can only contain letters and numbers")
    if pattern and not pattern.match(value):
        raise ValueError("Value does not match the required pattern")
    return value


def common_integer_range_validator(value: int | None, min_value: int, max_value: int, nullable: bool = False):
    if nullable and value is None:
        return value
    if not isinstance(value, int):
        raise TypeError(f"Value has to be an integer between {min_value} and {max_value}")
    if not (min_value <= value <= max_value):
        raise ValueError(f"Value has to be an integer between {min_value} and {max_value}")
    return value


def common_date_validator(value: datetime.date | None,
                          min_value: Optional[datetime.date] = None,
                          max_value: Optional[datetime.date] = None,
                          nullable: bool = False):
    if nullable and value is None:
        return value
    if not isinstance(value, datetime.date):
        raise TypeError("Value has to be a date")
    if min_value and value < min_value:
        raise ValueError(f"Value has to be after {min_value}")
    if max_value and value > max_value:
        raise ValueError(f"Value has to be before {max_value}")
    return value


def common_datetime_validator(value: datetime.datetime | None,
                              min_value: Optional[datetime.datetime] = None,
                              max_value: Optional[datetime.datetime] = None,
                              nullable: bool = False):
    if nullable and value is None:
        return value
    if not isinstance(value, datetime.datetime):
        raise TypeError("Value has to be a datetime")
    if min_value and value <= min_value:
        raise ValueError(f"Value has to be after {min_value}")
    if max_value and value > max_value:
        raise ValueError(f"Value has to be before {max_value}")
    return value
