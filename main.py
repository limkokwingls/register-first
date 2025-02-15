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



def main():
    display_students()


if __name__ == "__main__":
    main()
