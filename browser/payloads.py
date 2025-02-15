import datetime

from constants import CURRENT_TERM, INTAKE_DATE
from models import Student
from program_data import get_program, program_from_reference

date_format = "%Y-%m-%d"


def create_student_payload(student: Student) -> dict:
    program = program_from_reference(student.reference)
    if not program:
        raise ValueError("Program extracted from reference: ", student.reference)

    return {
        "x_InstitutionID": "1",
        "x_OthChgID": "OthChg0502",
        "x_IntakeDateCode": INTAKE_DATE,
        "x_StudentName": student.name,
        "x_StudentNo": student.national_id,
        "x_StudentStatus": "Active",
        "x_opSchoolID": program.school_id,
        "x_opProgramID": program.program_id,
        "x_opTermCode": CURRENT_TERM,
        "x_CountryCode": "LSO",
        "x_StdContactNo": student.phone1,
        "x_StdContactNo2": student.phone2,
        "x_StdEmail": student.email,
        "btnAction": "Add",
    }


def student_details_payload(std_no: str, std: Student) -> dict:
    if std.gender.upper() == "MALE":
        gender = "M"
    elif std.gender.upper() == "FEMALE":
        gender = "F"
    else:
        gender = "U"
    if std.marital_status.upper() == "SINGLE":
        marital_status = "S"
    elif std.marital_status.upper() == "MARRIED":
        marital_status = "M"
    else:
        marital_status = "U"

    return {
        "x_DateApplied": today(),
        "x_BirthDate": std.date_of_birth.strftime(date_format),
        "x_OfferTypeCode": "Full Acceptance",
        "x_ReligionCode": std.religion,
        "x_RaceCode": "African",
        "x_Nationality": "LSO",
        "x_Sex": gender,
        "x_MaritalStatus": marital_status,
        "x_CampusCode": "Lesotho",
        "x_StudentID": std_no,
        "x_EmergencyRelation": std.next_of_kin_relationship,
        "x_EmergencyContact": std.next_of_kin_name,
        "x_EmergencyNo": std.next_of_kin_phone,
        "btnAction": "Add",
    }


def register_program_payload(std_no: str, program_code: str) -> dict:
    program = get_program(program_code)
    if not program:
        raise ValueError("Program with code not found, code: ", program_code)
    return {
        "a_add": "A",
        "x_StudentID": std_no,
        "x_StdProgRegDate": today(),
        "x_ProgramID": program.program_id,
        "x_ProgramIntakeDate": INTAKE_DATE,
        "x_TermCode": CURRENT_TERM,
        "x_StructureID": program.version,
        "x_ProgStreamCode": "Normal",
        "x_ProgramStatus": "Active",
        "btnAction": "Add",
    }


def add_semester_payload(
    std_program_id: int, program_code: str, term: str, semester_id: str
) -> dict:
    program = get_program(program_code)
    if not program:
        raise ValueError("Program with code not found, code: ", program_code)
    return {
        "x_StdProgramID": std_program_id,
        "x_SchoolID": program.school_id,
        "x_ProgramID": program.program_id,
        "x_TermCode": term,
        "x_StructureID": program.version,
        "x_SemesterID": semester_id,
        "x_CampusCode": "Lesotho",
        "x_StdSemCAFDate": today(),
        "x_SemesterStatus": "Active",
        "btnAction": "Add",
    }


def add_update_payload(std_no: str) -> dict:
    return {
        "a_add": "A",
        "x_StudentID": std_no,
        "x_SuppObjectCode": "REG_SEMESTER",
        "btnAction": "Add",
    }


def today() -> str:
    return datetime.date.today().strftime("%Y-%m-%d")
