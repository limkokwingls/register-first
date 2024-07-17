import datetime
from datetime import date

from model import StudentInfo
from program_data import get_program

date_format = "%Y-%m-%d"


def create_student_payload(student_info: StudentInfo) -> dict:
    program = get_program(student_info.program.code)
    return {
        "x_InstitutionID": "1",
        "x_OthChgID": "OthChg0502",
        "x_IntakeDateCode": "2022-08-22",  # TODO: Change this to 2024-07-22
        "x_StudentName": student_info.names,
        "x_StudentNo": student_info.national_id,
        "x_StudentStatus": "Active",
        "x_opSchoolID": program.school_id,
        "x_opProgramID": program.program_id,
        "x_opTermCode": "2022-08",  # TODO: Change this to 2024-08
        "x_CountryCode": "LSO",
        "x_StdContactNo": student_info.phone1,
        "x_StdContactNo2": student_info.phone2,
        "x_StdEmail": student_info.email,
        "btnAction": "Add",
    }


def student_details_payload(std_no: str, std: StudentInfo) -> dict:
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
        "btnAction": "Add",
    }


def register_program_payload(std_no: str, program_code: str) -> dict:
    program = get_program(program_code)
    return {
        "a_add": "A",
        "x_StudentID": std_no,
        "x_StdProgRegDate": today(),
        "x_ProgramID": program.program_id,
        "x_ProgramIntakeDate": "2022-08-22",  # TODO: Change this to 2024-07-22
        "x_TermCode": "2022-08",  # TODO: Change this to 2024-08
        "x_StructureID": program.version,
        "x_ProgStreamCode": "Normal",
        "x_ProgramStatus": "Active",
        "btnAction": "Add",
    }


def today() -> str:
    return datetime.date.today().strftime("%Y-%m-%d")
