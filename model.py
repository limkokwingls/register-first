from dataclasses import dataclass, field
from typing import List, Literal, Optional
from datetime import date


@dataclass
class Program:
    name: str
    code: str
    faculty_code: str


@dataclass
class NextOfKin:
    name: str
    phone: str
    relationship: str


@dataclass
class StudentInfo:
    reference: str
    national_id: str
    names: str
    email: str
    confirm_email: str
    phone1: str
    phone2: Optional[str]
    religion: str
    date_of_birth: date
    gender: str
    marital_status: str
    birth_place: str
    home_town: str
    high_school: str
    program: Program
    next_of_kin: NextOfKin
