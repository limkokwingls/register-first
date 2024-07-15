import datetime

from model import StudentInfo
from program_codes import get_program
from datetime import date


def create_student_payload(student_info: StudentInfo) -> dict:
    program = get_program(student_info.program.code)
    return {
        "x_InstitutionID": '1',
        "x_OthChgID": 'OthChg0502',
        "x_IntakeDateCode": "2022-08-22",  #TODO: Change this to 2024-07-22
        "x_StudentName": student_info.names,
        "x_StudentNo": student_info.national_id,
        "x_StudentStatus": "Active",
        "x_opSchoolID": program["SchoolID"],
        "x_opProgramID": program["ProgramID"],
        "x_opTermCode": "2022-08",  #TODO: Change this to 2024-08
        "x_CountryCode": "LSO",
        "x_StdContactNo": student_info.phone1,
        "x_StdContactNo2": student_info.phone2,
        "x_StdEmail": student_info.email,
        "btnAction": "Add"
    }


def student_details_payload(std: StudentInfo) -> dict:
    date_format = "%Y-%m-%d"

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
        "x_DateApplied": date.today().strftime(date_format),
        "x_BirthDate": std.date_of_birth.strftime(date_format),
        "x_OfferTypeCode": "Full Acceptance",
        "x_ReligionCode": std.religion,
        "x_RaceCode": "African",
        "x_Nationality": "LSO",
        "x_Sex": gender,
        "x_MaritalStatus": marital_status,
        "x_CampusCode": "Lesotho",
    }
