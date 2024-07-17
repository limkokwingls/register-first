from dataclasses import dataclass, field
from typing import List, Literal, Optional
from datetime import date

from google.api_core.datetime_helpers import DatetimeWithNanoseconds


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
    std_no: str | None
    reference: str | None
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

    @classmethod
    def from_dict(cls, data):
        program = Program(
            name=data['program']['name'],
            code=data['program']['code'],
            faculty_code=data['program']['facultyCode']
        )

        next_of_kin = NextOfKin(
            name=data['nextOfKin']['names'],
            phone=data['nextOfKin']['phone'],
            relationship=data['nextOfKin']['relationship']
        )
        date_of_birth: DatetimeWithNanoseconds = data['dateOfBirth']

        return cls(
            std_no=data.get('stdNo'),
            reference=data['reference'],
            national_id=data['nationalId'],
            names=data['names'],
            email=data['email'],
            confirm_email=data['confirmEmail'],
            phone1=data['phone1'],
            phone2=data.get('phone2'),
            religion=data['religion'],
            date_of_birth=date_of_birth.date(),
            gender=data['gender'],
            marital_status=data['maritalStatus'],
            birth_place=data['birthPlace'],
            home_town=data['homeTown'],
            high_school=data['highSchool'],
            program=program,
            next_of_kin=next_of_kin
        )