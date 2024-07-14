from typing import Callable

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, \
    QSpacerItem, QSizePolicy
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
        self.id_input.input.textChanged.connect(self.enable_lookup)
        self.reference_no = InputField("Reference No.")
        self.reference_no.input.textChanged.connect(self.enable_lookup)
        self.lookup_button = QPushButton("Look Up")
        self.lookup_button.setDisabled(True)
        self.lookup_button.clicked.connect(self.lookup)
        self.lookup_button.setMinimumSize(100, 30)
        button_layout = QVBoxLayout()
        button_layout.addItem(QSpacerItem(0, 20))
        button_layout.addWidget(self.lookup_button)

        layout = QHBoxLayout()
        layout.addWidget(self.id_input)
        layout.addWidget(self.reference_no)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def enable_lookup(self):
        if len(self.id_input.input.text()) > 1 or len(self.reference_no.input.text()) > 1:
            self.lookup_button.setDisabled(False)
        else:
            self.lookup_button.setDisabled(True)

    def lookup(self):
        self.lookup_button.setDisabled(True)
        try:
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
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            self.lookup_button.setDisabled(False)
