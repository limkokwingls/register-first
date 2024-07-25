from dataclasses import dataclass, field
from typing import List, Literal, Optional
from datetime import date

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


@dataclass
class StudentInfo:
    doc_id: str | None
    std_no: str | None
    reference: str | None
    national_id: str
    names: str
    email: str
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
    def from_dict(cls, data, doc_id):
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
        date_of_birth = data['dateOfBirth']
        if isinstance(date_of_birth, DatetimeWithNanoseconds):
            date_of_birth = date_of_birth.date()
        elif isinstance(date_of_birth, str):
            date_of_birth = date.fromisoformat(date_of_birth)

        return cls(
            doc_id=doc_id,
            std_no=data.get('stdNo'),
            reference=data['reference'],
            national_id=data['nationalId'],
            names=data['names'],
            email=data['email'],
            phone1=data['phone1'],
            phone2=data.get('phone2'),
            religion=data['religion'],
            date_of_birth=date_of_birth,
            gender=data['gender'],
            marital_status=data['maritalStatus'],
            birth_place=data['birthPlace'],
            home_town=data['homeTown'],
            high_school=data['highSchool'],
            program=program,
            next_of_kin=next_of_kin
        )

    def to_dict(self):
        return {
            "stdNo": self.std_no,
            "reference": self.reference,
            "nationalId": self.national_id,
            "names": self.names,
            "email": self.email,
            "confirmEmail": self.confirm_email,
            "phone1": self.phone1,
            "phone2": self.phone2,
            "religion": self.religion,
            "dateOfBirth": self.date_of_birth.isoformat(),
            "gender": self.gender,
            "maritalStatus": self.marital_status,
            "birthPlace": self.birth_place,
            "homeTown": self.home_town,
            "highSchool": self.high_school,
            "program": {
                "name": self.program.name,
                "code": self.program.code,
                "facultyCode": self.program.faculty_code
            },
            "nextOfKin": {
                "names": self.next_of_kin.name,
                "phone": self.next_of_kin.phone,
                "relationship": self.next_of_kin.relationship
            }
        }