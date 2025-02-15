from dataclasses import dataclass, field
from datetime import date
from typing import List, Literal, Optional

from google.api_core.datetime_helpers import DatetimeWithNanoseconds


@dataclass
class Program:
    name: str
    code: str
    faculty_code: str
    bhr_year: Optional[str] = None


@dataclass
class NextOfKin:
    name: str
    phone: str
    relationship: str
