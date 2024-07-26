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
        code="BAAS",
        program_id=170,
        name="BA in Architectural Studies",
        version=518,
    ),
    Program(
        school_id=3,
        faculty="FABE",
        code="CAT",
        program_id=164,
        name="Certificate in Architectural Technology",
        version=509,
    ),
    Program(
        school_id=3,
        faculty="FABE",
        code="DAT",
        program_id=138,
        name="Diploma in Architecture Technology",
        version=493,
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
        school_id=4,
        faculty="FDI",
        code="DCAV",
        program_id=160,
        name="Diploma in Creative Advertising",
        version=486,
    ),
    Program(
        school_id=4,
        faculty="FDI",
        code="DGD",
        program_id=159,
        name="Diploma in Graphic Design",
        version=487,
    ),
    Program(
        school_id=5,
        faculty="FBMG",
        code="BEN",
        program_id=136,
        name="B Bus in Entrepreneurship",
        version=503,
        # version=531
    ),
    Program(
        school_id=5,
        faculty="FBMG",
        code="BHR",
        program_id=137,  # Todo: Handle HR Advanced
        name="BA in Human Resource Management",
        version=528,
    ),
    Program(
        school_id=5,
        faculty="FBMG",
        code="BIB",
        program_id=135,
        name="B Bus in International Business",
        version=505,
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
        school_id=5,
        faculty="FBMG",
        code="DBM",
        program_id=130,
        name="Diploma in Business Management",
        version=499,
    ),
    Program(
        school_id=5,
        faculty="FBMG",
        code="DMK",
        program_id=131,
        name="Diploma in Marketing",
        version=500,
    ),
    Program(
        school_id=5,
        faculty="FBMG",
        code="DRM",
        program_id=134,
        name="Diploma in Retail Management",
        version=498,
    ),
    Program(
        school_id=7,
        faculty="FCMB",
        code="BPC",
        program_id=142,
        name="BA in Professional Communication",
        version=491,
    ),
    Program(
        school_id=7,
        faculty="FCMB",
        code="DJM",
        program_id=141,
        name="Diploma in Journalism & Media",
        version=506,
    ),
    Program(
        school_id=7,
        faculty="FCMB",
        code="DPR",
        program_id=140,
        name="Diploma in Public Relations",
        version=490,
    ),
    Program(
        school_id=8,
        faculty="FICT",
        code="BSCBIT",
        program_id=155,
        name="BSc in Business Information Technology",
        version=521,
    ),
    Program(
        school_id=8,
        faculty="FICT",
        code="BSCIT",
        program_id=154,
        name="BSc in Information Technology",
        version=520,
    ),
    Program(
        school_id=8,
        faculty="FICT",
        code="BSCSM",
        program_id=156,
        name="BSc in Software Engineering with Multimedia",
        version=522,
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
        school_id=8,
        faculty="FICT",
        code="DBIT",
        program_id=152,
        name="Diploma in Business Information Technology",
        version=524,
    ),
    Program(
        school_id=8,
        faculty="FICT",
        code="DIT",
        program_id=151,
        name="Diploma in Information Technology",
        version=523,
    ),
    Program(
        school_id=8,
        faculty="FICT",
        code="DMSE",
        program_id=153,
        name="Diploma in Multimedia & Software Engineering",
        version=525,
    ),
    Program(
        school_id=10,
        faculty="FDI",
        code="BAFASH",
        program_id=158,
        name="BA in Fashion & Retailing",
        version=489,
    ),
    Program(
        school_id=10,
        faculty="FDI",
        code="DFAD",
        program_id=157,
        name="Diploma in Fashion & Apparel Design",
        version=488,
    ),
    Program(
        school_id=15,
        faculty="FCMB",
        code="BBJ",
        program_id=145,
        name="BA in Broadcasting & Journalism",
        version=492,
        # version=529,
    ),
    Program(
        school_id=15,
        faculty="FCMB",
        code="BDF",
        program_id=146,
        name="BA in Digital Film Production",
        version=510,
        # version=527
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
        school_id=15,
        faculty="FCMB",
        code="DBRTV",
        program_id=143,
        name="Diploma in Broadcasting Radio & TV",
        version=504,
    ),
    Program(
        school_id=15,
        faculty="FCMB",
        code="DFP",
        program_id=144,
        name="Diploma in Film Production",
        version=508,
    ),
    Program(
        school_id=16,
        faculty="FCTH",
        code="BTM",
        program_id=162,
        name="BA in Tourism Management",
        version=484,
    ),
    Program(
        school_id=16,
        faculty="FCTH",
        code="CITM",
        program_id=167,
        name="Certificate in Innovative Travel & Tourism",
        version=514,
    ),
    Program(
        school_id=16,
        faculty="FCTH",
        code="DEM",
        program_id=150,
        name="Diploma in Events Management",
        version=485,
    ),
    Program(
        school_id=16,
        faculty="FCTH",
        code="DHM",
        program_id=148,
        name="Diploma in Hotel Management",
        version=483,
    ),
    Program(
        school_id=16,
        faculty="FCTH",
        code="DTM",
        program_id=147,
        name="Diploma in Tourism Management",
        version=482,
    ),
]


def get_program(code: str) -> Program | None:
    return next(
        (program for program in __data if program.code == code), None
    )


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
