from typing import Callable

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from google.cloud.firestore_v1 import FieldFilter

from config.firebase import db
from model import StudentInfo


class InputField(QWidget):
    def __init__(self, label: str):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.label = QLabel(label)
        self.input = QLineEdit()
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.input)


class LookupWidget(QWidget):
    def __init__(self, handle_response: Callable[[StudentInfo | None], None]):
        super().__init__()
        self.handle_response = handle_response
        self.id_input = InputField("National Id")
        self.reference_no = InputField("Reference No.")
        self.lookup_button = QPushButton("Look Up")
        self.lookup_button.clicked.connect(self.lookup)

        layout = QHBoxLayout()
        layout.addWidget(self.id_input)
        layout.addWidget(self.reference_no)
        layout.addWidget(self.lookup_button)
        self.setLayout(layout)

    def lookup(self):
        text = self.id_input.input.text()
        docs = (
            db.collection("registrations")
            .where(filter=FieldFilter("nationalId", "==", text))
            .get()
        )
        student_info = None
        if docs:
            student_info = StudentInfo.from_dict(docs[0].to_dict())
        self.handle_response(student_info)

