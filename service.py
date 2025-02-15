import traceback

from rich import print
from sqlalchemy.orm import Session

from browser import Browser
from models import Student
from program_data import Program

browser = Browser()


class RegisterService:

    def __init__(self, db: Session, student: Student, program: Program):
        self.db = db
        self.student = student
        self.program = program

    def register_student(self):
        try:
            browser = Browser()
            browser.check_logged_in()
            
            print(f"\nProcessing student registration...")
            std_no = browser.create_student(self.student)
            if not std_no:
                print("❌ Failed to create student record")
                return

            print(f"✅ Created student [{std_no}]")
            if not browser.add_student_details(std_no, self.student):
                print("❌ Failed to add student details")
                return

            print(f"✅ Added personal details")
            std_program_id = browser.register_program(std_no, self.program.code)
            if not std_program_id:
                print(f"✅ Failed to register program {self.program.code}")
                return

            print(f"✅ Registered program {self.program.code}")
            std_semester_id = browser.add_semester(std_program_id, self.program)
            if not std_semester_id:
                print("❌ Failed to add semester")
                return

            browser.add_modules(std_semester_id)
            browser.add_update(std_no)
            self.save_student_number(id=self.student.id, std_num=std_no)
            print(f"✅ Completed registration for student [{std_no}]")
            
        except Exception as e:
            print(f"❌ Registration failed: {str(e)}")
            traceback.print_exc()

    def save_student_number(self, id: str, std_num: str):
        student = self.db.query(Student).get(id)
        if student:
            student.std_no = std_num
            self.db.add(student)
            self.db.commit()
            print(f"✅ Saved student number {std_num} for student {id}\n")
        else:
            print(f"❌ Student with id {id} not found in database")