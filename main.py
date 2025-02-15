from sqlalchemy import func

from config.database import SessionLocal
from models import Base, Student
from program_data import program_from_reference

CURRENT_TERM = "2025-02"
INTAKE_DATE = "2025-02-03"


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def display_students():
    db = get_db()
    students = (
        db.query(Student).filter(Student.paid == True, Student.std_no.is_(None)).all()
    )

    print("\nAll Students:")
    print("-" * 80)
    print(f"{'ID':<5} {'Reference':<15} {'Name':<25} {'Program':<20}")
    print("-" * 80)

    for student in students:
        program = program_from_reference(student.reference)
        print(
            f"{student.id:<5} {student.reference:<15} {student.name:<25} {program.name:<20}"
        )

    print("-" * 80)
    print(f"Total Students: {len(students)}")


def main():
    display_students()


if __name__ == "__main__":
    main()
