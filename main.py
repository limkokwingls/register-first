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


def register_students():
    db = get_db()
    students = (
        db.query(Student).filter(Student.paid == True, Student.std_no.is_(None)).all()
    )

    if not students:
        print("No pending student registrations found.")
        return

    total_students = len(students)
    print(f"\nProcessing {total_students} pending student(s)...\n")
    
    for index, student in enumerate(students, 1):
        print(f"[{index}/{total_students}] Processing student: {student.name}")
        try:
            program = program_from_reference(student.reference)
            if not program:
                print(f"⚠️  Error: Program not found for student {student.name} (Reference: {student.reference})")
                continue
                
            service = RegisterService(db, student, program)
            service.register_student()
            
        except Exception as e:
            print(f"❌ Failed to register {student.name}: {str(e)}\n")


def display_students():
    db = get_db()

    students = (
        db.query(Student).filter(Student.paid == True, Student.std_no.isnot(None)).all()
    )
    total_students = len(students)
    print(f"\nDisplaying {total_students} registered student(s):\n")
    
    print(f"{'Student Number':<15} {'Name':<30}")
    print("-" * 45)
    for student in students:
        print(f"{student.std_no:<15} {student.name:<30}")


def main():
    display_students()


if __name__ == "__main__":
    main()
