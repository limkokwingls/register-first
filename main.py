from sqlalchemy.orm import sessionmaker

from config.database import SessionLocal, engine
from models import Base, Student


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def display_students():
    db = get_db()
    students = db.query(Student).all()
    
    print("\nAll Students:")
    print("-" * 80)
    print(f"{'ID':<5} {'Reference':<15} {'Name':<25} {'Student No':<12} {'Program':<20}")
    print("-" * 80)
    
    for student in students:
        print(f"{student.id:<5} {student.reference:<15} {student.names:<25} {student.std_no or 'N/A':<12} {student.program.name:<20}")
    
    print("-" * 80)
    print(f"Total Students: {len(students)}")


def main():
    display_students()


if __name__ == "__main__":
    main()
