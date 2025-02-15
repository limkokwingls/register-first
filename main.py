from sqlalchemy import func

from config.database import SessionLocal
from models import Base, Student
from program_data import program_from_reference
from service import RegisterService


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

    if not students:
        print("No pending student registrations found.")
        return

    print(f"Processing {len(students)} pending student(s)...")
    
    for student in students:
        program = program_from_reference(student.reference)
        if not program:
            raise ValueError("Program not found from reference:", student.reference)
        service = RegisterService(db, student, program)
        service.register_student()
        exit()


def main():
    display_students()


if __name__ == "__main__":
    main()
