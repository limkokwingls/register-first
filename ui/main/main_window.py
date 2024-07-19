from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QTableWidget, QHeaderView,
                               QTableWidgetItem, QLabel)
from google.cloud.firestore_v1 import FieldFilter, aggregation

from config.firebase import db
from ui.form.student_form import StudentForm
from ui.main.LookupWidget import LookupWidget


class FirestoreSignals(QObject):
    dataChanged = Signal(list)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.firestore_signals = FirestoreSignals()
        self.firestore_signals.dataChanged.connect(self.update_table)

        lookup = LookupWidget(handle_response)

        layout = QVBoxLayout()
        layout.addWidget(lookup)
        central = QWidget()
        central.setLayout(layout)

        self.setCentralWidget(central)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.total_label = QLabel("Registered Students: ?")
        self.table.setHorizontalHeaderLabels(["Student No.", "Name", "National ID", "Program"])
        layout.addWidget(self.total_label)
        layout.addWidget(self.table)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.resize(980, 600)

        # Set up Firestore listener
        self.setup_firestore_listener()

        # Fetch and display total students count
        self.update_total_students()

    def setup_firestore_listener(self):
        students_ref = db.collection('registrations').where(filter=FieldFilter(
            field_path='stdNo', op_string='>', value=0
        ))
        students_ref.on_snapshot(self.on_snapshot)

    def on_snapshot(self, doc_snapshot, changes, read_time):
        students = []
        for doc in doc_snapshot:
            student_data = doc.to_dict()
            students.append(student_data)
        self.firestore_signals.dataChanged.emit(students)

    def update_table(self, students):
        self.table.setRowCount(len(students))
        for row, student in enumerate(students):
            self.table.setItem(row, 0, QTableWidgetItem(str(student.get('stdNo', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(student.get('names', '')))
            self.table.setItem(row, 2, QTableWidgetItem(student.get('nationalId', '')))
            self.table.setItem(row, 3, QTableWidgetItem(student.get('program', '').get('name')))

        self.update_total_students()

    def update_total_students(self):
        query = db.collection('registrations').where(filter=FieldFilter(
            field_path='stdNo', op_string='>', value=0
        ))
        aggregate_query = aggregation.AggregationQuery(query)
        aggregate_query.count(alias="count")

        count = aggregate_query.get()[0][0]
        self.total_label.setText(f"Registered Students: {count.value}")


def handle_response(student_info):
    form = StudentForm(student_info)
    form.exec()
