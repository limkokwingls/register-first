from PySide6.QtCore import QDate, QThread
from PySide6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QDateEdit,
                               QComboBox, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel)

from model import StudentInfo, Program, NextOfKin
from program_data import get_faculty_codes, get_program_names, get_program_code
from ui.form.save_worker import SaveWorker


class StudentForm(QDialog):
    def __init__(self, student_info: StudentInfo = None):
        super().__init__()
        self.worker = None
        self.thread = None
        self.setWindowTitle("Student Information")
        self.setMinimumWidth(500)

        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.national_id = QLineEdit()
        self.names = QLineEdit()
        self.email = QLineEdit()
        self.confirm_email = QLineEdit()
        self.phone1 = QLineEdit()
        self.phone2 = QLineEdit()
        self.religion = QLineEdit()
        self.date_of_birth = QDateEdit()
        self.date_of_birth.setDisplayFormat("yyyy-MM-dd")
        self.gender = QComboBox()
        self.gender.addItems(["Male", "Female", "Other"])
        self.marital_status = QComboBox()
        self.marital_status.addItems(["Single", "Married", "Divorced", "Widowed", "Other"])
        self.birth_place = QLineEdit()
        self.home_town = QLineEdit()
        self.high_school = QLineEdit()

        form_layout.addRow("National ID:", self.national_id)
        form_layout.addRow("Names:", self.names)
        form_layout.addRow("Email:", self.email)
        form_layout.addRow("Confirm Email:", self.confirm_email)
        form_layout.addRow("Phone 1:", self.phone1)
        form_layout.addRow("Phone 2:", self.phone2)
        form_layout.addRow("Religion:", self.religion)
        form_layout.addRow("Date of Birth:", self.date_of_birth)
        form_layout.addRow("Gender:", self.gender)
        form_layout.addRow("Marital Status:", self.marital_status)
        form_layout.addRow("Birth Place:", self.birth_place)
        form_layout.addRow("Home Town:", self.home_town)
        form_layout.addRow("High School:", self.high_school)

        # Program Information
        program_group = QGroupBox("Program")
        program_layout = QFormLayout()
        self.faculty_code = QComboBox()
        self.faculty_code.addItems(get_faculty_codes())
        self.faculty_code.currentIndexChanged.connect(self.handle_faculty_change)
        self.program_name = QComboBox()
        self.program_name.addItems(get_program_names(self.faculty_code.currentText()))
        self.program_name.currentIndexChanged.connect(
            lambda: self.program_code.setText(get_program_code(self.program_name.currentText()))
        )
        self.program_code = QLineEdit()
        self.program_code.setReadOnly(True)
        program_layout.addRow("Faculty Code:", self.faculty_code)
        program_layout.addRow("Name:", self.program_name)
        program_layout.addRow("Code:", self.program_code)
        program_group.setLayout(program_layout)

        # Next of Kin Information
        next_of_kin_group = QGroupBox("Next of Kin")
        next_of_kin_layout = QFormLayout()
        self.next_of_kin_name = QLineEdit()
        self.next_of_kin_phone = QLineEdit()
        self.next_of_kin_relationship = QLineEdit()
        next_of_kin_layout.addRow("Name:", self.next_of_kin_name)
        next_of_kin_layout.addRow("Phone:", self.next_of_kin_phone)
        next_of_kin_layout.addRow("Relationship:", self.next_of_kin_relationship)
        next_of_kin_group.setLayout(next_of_kin_layout)

        main_layout.addLayout(form_layout)
        main_layout.addWidget(program_group)
        main_layout.addWidget(next_of_kin_group)

        # Buttons
        footer = QHBoxLayout()
        self.status_label = QLabel()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_student_info)
        footer.addWidget(self.status_label, 3)
        footer.addWidget(self.save_button, 1)
        main_layout.addLayout(footer)

        self.setLayout(main_layout)

        if student_info:
            self.populate_form(student_info)

    def handle_faculty_change(self):
        self.program_name.clear()
        self.program_name.addItems(get_program_names(self.faculty_code.currentText()))

    def populate_form(self, student_info: StudentInfo):
        self.national_id.setText(student_info.national_id)
        self.names.setText(student_info.names)
        self.email.setText(student_info.email)
        self.confirm_email.setText(student_info.confirm_email)
        self.phone1.setText(student_info.phone1)
        self.phone2.setText(student_info.phone2 or "")
        self.religion.setText(student_info.religion)
        self.date_of_birth.setDate(QDate(student_info.date_of_birth))
        self.gender.setCurrentText(student_info.gender)
        self.marital_status.setCurrentText(student_info.marital_status)
        self.birth_place.setText(student_info.birth_place)
        self.home_town.setText(student_info.home_town)
        self.high_school.setText(student_info.high_school)

        self.faculty_code.setCurrentText(student_info.program.faculty_code)
        self.program_name.setCurrentText(student_info.program.name)
        self.program_code.setText(student_info.program.code)

        self.next_of_kin_name.setText(student_info.next_of_kin.name)
        self.next_of_kin_phone.setText(student_info.next_of_kin.phone)
        self.next_of_kin_relationship.setText(student_info.next_of_kin.relationship)

    def save_student_info(self):
        self.save_button.setEnabled(False)

        student = self.from_form()
        self.worker = SaveWorker(student)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.save)
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.on_save_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def on_save_finished(self, success, message):
        self.save_button.setEnabled(True)
        if success:
            self.status_label.setText(f"Student saved successfully! Student number: {message}")
        else:
            self.status_label.setText(f"Error saving student information: {message}")

    def from_form(self) -> StudentInfo:
        program = Program(
            name=self.program_name.text(),
            code=self.program_code.text(),
            faculty_code=self.faculty_code.text()
        )

        next_of_kin = NextOfKin(
            name=self.next_of_kin_name.text(),
            phone=self.next_of_kin_phone.text(),
            relationship=self.next_of_kin_relationship.text()
        )

        return StudentInfo(
            reference=None,
            national_id=self.national_id.text(),
            names=self.names.text(),
            email=self.email.text(),
            confirm_email=self.confirm_email.text(),
            phone1=self.phone1.text(),
            phone2=self.phone2.text() if self.phone2.text() else None,
            religion=self.religion.text(),
            date_of_birth=self.date_of_birth.date().toPython(),
            gender=self.gender.currentText(),
            marital_status=self.marital_status.currentText(),
            birth_place=self.birth_place.text(),
            home_town=self.home_town.text(),
            high_school=self.high_school.text(),
            program=program,
            next_of_kin=next_of_kin
        )
