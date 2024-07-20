import logging
from typing import Callable

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, \
    QSpacerItem
from google.cloud.firestore_v1 import FieldFilter, Or

from config.firebase import db
from model import StudentInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InputField(QWidget):
    def __init__(self, label: str, value: str = ""):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.label = QLabel(label)
        self.input = QLineEdit(value)
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.input)


class LookupWidget(QWidget):
    def __init__(self, handle_response: Callable[[StudentInfo | None], None]):
        super().__init__()
        self.handle_response = handle_response
        self.id_input = InputField("National Id")
        self.id_input.input.textChanged.connect(self.enable_lookup)
        self.id_input.input.returnPressed.connect(self.enable_lookup)
        self.id_input.input.returnPressed.connect(self.lookup)
        self.reference_no = InputField("Reference No.", "LUCT/")
        self.reference_no.input.textChanged.connect(self.enable_lookup)
        self.reference_no.input.returnPressed.connect(self.enable_lookup)
        self.reference_no.input.returnPressed.connect(self.lookup)
        self.lookup_button = QPushButton("Look Up")
        self.lookup_button.setDisabled(True)
        self.lookup_button.clicked.connect(self.lookup)
        self.lookup_button.setMaximumSize(100, 30)
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
        reference_no = self.reference_no.input.text().lower().replace("/", "-").strip()
        national_id = self.id_input.input.text().strip()
        logger.info(f"Looking up student by national id no. '{national_id}' or reference no. '{reference_no}'")
        try:
            filter_1 = FieldFilter("nationalId", "==", national_id)
            filter_2 = FieldFilter("reference", "==", reference_no)

            docs = (
                db.collection("registrations")
                .where(filter=Or(filters=[filter_1, filter_2]))
                .get()
            )
            student_info = None
            if docs:
                logger.info(f"Found {len(docs)} student(s)")
                student_info = StudentInfo.from_dict(docs[0].to_dict(), docs[0].id)
            else:
                logger.warning("No student found")
            self.handle_response(student_info)
        except Exception as e:
            logger.error(e)
            QMessageBox.critical(self, "Error", str(e))
        finally:
            self.lookup_button.setDisabled(False)
