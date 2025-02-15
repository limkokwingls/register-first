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
            print("Initializing...")
            browser = Browser()
            browser.check_logged_in()
            print("Creating student...")
            std_no = browser.create_student(self.student)

            if std_no:
                print(f"{std_no} | Adding student details...")
                success = browser.add_student_details(std_no, self.student)
                if success:
                    print(f"{std_no} | Registering for {self.program.code}...")
                    std_program_id = browser.register_program(std_no, self.program.code)
                    if std_program_id:
                        print(f"{std_no} | Adding semester...")
                        std_semester_id = browser.add_semester(
                            std_program_id,
                            self.program,
                        )
                        if std_semester_id:
                            print(f"{std_no} | Adding modules...")
                            browser.add_modules(std_semester_id)
                            print(f"{std_no} | Updating semester registration...")
                            browser.add_update(std_no)
                            print(f"{std_no} | Updating database...")
                            self.save_student_number(
                                id=self.student.id,
                                std_num=std_no,
                            )
                        else:
                            print("Failed to add semester")
            else:
                print("Failed to create student")
        except Exception as e:
            print(f"Error saving student: {e}")
            traceback.print_exc()

    def save_student_number(self, id: str, std_num: str):
        student = self.db.query(Student).get(id)
        if student:
            student.std_no = std_num
            self.db.add(student)
            self.db.commit()
        else:
            print("Student with id", id, " not found")