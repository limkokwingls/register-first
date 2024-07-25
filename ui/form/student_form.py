from PySide6.QtCore import QDate, QThread
from PySide6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QDateEdit,
                               QComboBox, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QProgressBar,
                               QMessageBox, QRadioButton, QButtonGroup)

from model import StudentInfo, Program, NextOfKin
from program_data import get_faculty_codes, get_program_names, get_program_code
from ui.form.save_worker import SaveWorker
import pyperclip


class StudentForm(QDialog):
    def __init__(self, student_info: StudentInfo = None):
        super().__init__()
        self.doc_id = student_info.doc_id if student_info else None
        self.worker = None
        self.thread = None
        self.setWindowTitle("Student Information")
        self.setMinimumWidth(500)

        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.national_id = QLineEdit()
        self.names = QLineEdit()
        self.email = QLineEdit()
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
        self.progress_bar = QProgressBar()

        form_layout.addRow("National ID:", self.national_id)
        form_layout.addRow("Names:", self.names)
        form_layout.addRow("Email:", self.email)
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
        self.program_name.currentIndexChanged.connect(self.handle_program_change)
        self.program_code = QLineEdit()
        self.program_code.setReadOnly(True)

        self.bhr_options_group = QGroupBox("BHR Options")
        self.bhr_options_group.setVisible(False)
        bhr_options_layout = QHBoxLayout()
        self.bhr_first_year = QRadioButton("First Year")
        self.bhr_advanced = QRadioButton("Advanced")
        self.bhr_button_group = QButtonGroup()
        self.bhr_button_group.addButton(self.bhr_first_year)
        self.bhr_button_group.addButton(self.bhr_advanced)
        bhr_options_layout.addWidget(self.bhr_first_year)
        bhr_options_layout.addWidget(self.bhr_advanced)
        self.bhr_options_group.setLayout(bhr_options_layout)

        program_layout.addRow("Faculty Code:", self.faculty_code)
        program_layout.addRow("Name:", self.program_name)
        program_layout.addRow("Code:", self.program_code)
        program_layout.addRow(self.bhr_options_group)
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

        main_layout.addWidget(self.progress_bar)

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

    def handle_program_change(self):
        program_code = get_program_code(self.program_name.currentText())
        self.program_code.setText(program_code)
        self.bhr_options_group.setVisible(program_code == "BHR")
        if program_code != "BHR":
            self.bhr_button_group.setExclusive(False)
            self.bhr_first_year.setChecked(False)
            self.bhr_advanced.setChecked(False)
            self.bhr_button_group.setExclusive(True)

    def populate_form(self, student_info: StudentInfo):
        self.national_id.setText(student_info.national_id)
        self.names.setText(format_name(student_info.names))
        self.email.setText(student_info.email.lower())
        self.phone1.setText(format_phone(student_info.phone1))
        self.phone2.setText(format_phone(student_info.phone2))
        self.religion.setText(student_info.religion)
        self.date_of_birth.setDate(QDate(student_info.date_of_birth))
        self.gender.setCurrentText(student_info.gender)
        self.marital_status.setCurrentText(student_info.marital_status)
        self.birth_place.setText(format_place(student_info.birth_place))
        self.home_town.setText(format_place(student_info.home_town))
        self.high_school.setText(format_place(student_info.high_school))

        self.faculty_code.setCurrentText(student_info.program.faculty_code)
        self.program_name.setCurrentText(student_info.program.name)
        self.program_code.setText(student_info.program.code)

        self.next_of_kin_name.setText(format_name(student_info.next_of_kin.name))
        self.next_of_kin_phone.setText(format_phone(student_info.next_of_kin.phone))
        self.next_of_kin_relationship.setText(student_info.next_of_kin.relationship)

        self.handle_program_change()

        if student_info.program.code == "BHR":
            if student_info.program.bhr_year == "First Year":
                self.bhr_first_year.setChecked(True)
            elif student_info.program.bhr_year == "Advanced":
                self.bhr_advanced.setChecked(True)

    def save_student_info(self):
        if self.program_code.text() == "BHR" and not self.bhr_button_group.checkedButton():
            QMessageBox.warning(self, "Incomplete Form", "Please select a BHR option (First Year or Advanced).")
            return

        self.save_button.setEnabled(False)

        student = self.from_form()
        self.worker = SaveWorker(student)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.save)
        self.worker.message.connect(self.update_status)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_save_finished)
        self.worker.finished.connect(self.thread.quit)

        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def on_progress(self, value: int):
        self.progress_bar.setValue(value)
        if value > 0:
            self.progress_bar.setRange(0, 8)
        else:
            self.progress_bar.setRange(0, 0)

    def on_save_finished(self, success, message):
        self.save_button.setEnabled(True)
        if success:
            QMessageBox.information(self, "Success", f"Student registration successful!\nStudent No: {message}")
            pyperclip.copy(message)
            self.close()
        else:
            self.status_label.setText(f"Error saving student information: {message}")

    def from_form(self) -> StudentInfo:
        hr_option = self.bhr_button_group.checkedButton().text() if self.program_code.text() == "BHR" else None
        bhr_year = None
        if hr_option:
            if hr_option == "Advanced":
                bhr_year = "Year 2 Sem 1"
            else:
                bhr_year = "Year 1 Sem 1"

        program = Program(
            name=self.program_name.currentText(),
            code=self.program_code.text(),
            faculty_code=self.faculty_code.currentText(),
            bhr_year=bhr_year
        )

        next_of_kin = NextOfKin(
            name=self.next_of_kin_name.text(),
            phone=self.next_of_kin_phone.text(),
            relationship=self.next_of_kin_relationship.text()
        )

        return StudentInfo(
            doc_id=self.doc_id,
            std_no=None,
            reference=None,
            national_id=self.national_id.text(),
            names=self.names.text(),
            email=self.email.text(),
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


def format_place(name: str | None) -> str | None:
    if not name:
        return None
    parts = name.split()
    for i, part in enumerate(parts):
        if part.lower() in ["of", "the", "and", "at", "in", "on", "for", "to", "by", "with", "from"]:
            parts[i] = part.lower()
        elif "." in part:
            parts[i] = part
        else:
            parts[i] = part.capitalize()
    return " ".join(parts).strip()


def format_phone(phone: str | None) -> str:
    if not phone:
        return ""
    phone = phone.replace(" ", "").strip()
    if len(phone) == 8:
        return f"+266{phone}"
    return phone.strip()


def format_name(name: str | None) -> str | None:
    if not name:
        return None
    return " ".join([part.capitalize() for part in name.split()]).strip()
