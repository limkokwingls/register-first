from dataclasses import dataclass
from typing import List


@dataclass
class Program:
    school_id: int
    faculty: str
    code: str
    program_id: int
    name: str
    version: int


__data = [
    Program(
        school_id=3,
        faculty="FABE",
        code="CAT",
        program_id=164,
        name="Certificate in Architectural Technology",
        version=509,
    ),
    Program(
        school_id=4,
        faculty="FDI",
        code="CGD",
        program_id=165,
        name="Certificate in Graphic Design",
        version=512,
    ),
    Program(
        school_id=5,
        faculty="FBMG",
        code="CMK",
        program_id=166,
        name="Certificate in Marketing",
        version=513,
    ),
    Program(
        school_id=8,
        faculty="FICT",
        code="CBIT",
        program_id=163,
        name="Certificate in Business Information Technology",
        version=526,
    ),
    Program(
        school_id=15,
        faculty="FCMB",
        code="CPA",
        program_id=171,
        name="Certificate in Performing Arts",
        version=519,
    ),
    Program(
        school_id=15,
        faculty="FCMB",
        code="CRB",
        program_id=169,
        name="Certificate in Radio Broadcasting",
        version=517,
    ),
    Program(
        school_id=16,
        faculty="FCTH",
        code="CITM",
        program_id=167,
        name="Certificate in Innovative Travel & Tourism",
        version=514,
    ),
]


def get_program(code: str) -> Program | None:
    return next((program for program in __data if program.code == code), None)

def program_from_reference(reference: str | None) -> Program | None:
    if not reference:
        raise ValueError("Reference cannot be empty")
    code = reference.split("-")[1].upper()
    if code in ["CITT", "CTM"]:
        code = "CITM"
    return get_program(code)

def get_program_names(faculty: str | None) -> List[str]:
    if not faculty:
        return [program.name for program in __data]
    return [program.name for program in __data if program.faculty == faculty]


def get_faculty_codes() -> List[str]:
    return list(set([program.faculty for program in __data]))


def get_program_code(name: str) -> str:
    program = next((program for program in __data if program.name == name), None)
    return program.code if program else ""


def faculty_of(self, code: str) -> str:
    program = self.get_program(code)
    return program.faculty if program else ""
