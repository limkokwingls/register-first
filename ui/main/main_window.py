from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QHeaderView,
    QLabel,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget,
)
from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Student
from ui.form.student_form import StudentForm
from ui.main.LookupWidget import LookupWidget
from ui.main.settings_dialog import SettingsDialog


class DatabaseSignals(QObject):
    dataChanged = Signal(list)


class MainWindow(QMainWindow):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self.db_signals = DatabaseSignals()
        self.db_signals.dataChanged.connect(self.update_table)

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(lambda: handle_response(None))
        file_menu.addAction(new_action)
        menu.addMenu(file_menu)

        lookup = LookupWidget(self.session, handle_response)

        layout = QVBoxLayout()
        layout.addWidget(lookup)
        central = QWidget()
        central.setLayout(layout)

        self.setCentralWidget(central)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.total_label = QLabel("Registered Students: ?")
        self.table.setHorizontalHeaderLabels(
            ["Student No.", "Name", "National ID", "Program"]
        )
        layout.addWidget(self.total_label)
        layout.addWidget(self.table)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings_dialog)
        file_menu.addAction(settings_action)

        self.resize(980, 600)

        self.setup_data_listener()
        self.update_total_students()

    def open_settings_dialog(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def setup_data_listener(self):
        students = (
            self.session.query(Student)
            .filter(Student.std_no.isnot(None))
            .order_by(Student.std_no.desc())
            .limit(20)
            .all()
        )
        self.db_signals.dataChanged.emit([s.to_dict() for s in students])

    def update_table(self, students):
        # order by stdNo descending
        students.sort(key=lambda x: x.get("stdNo", 0), reverse=True)
        self.table.setRowCount(len(students))
        for row, student in enumerate(students):
            self.table.setItem(row, 0, QTableWidgetItem(str(student.get("stdNo", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(student.get("names", "")))
            self.table.setItem(row, 2, QTableWidgetItem(student.get("nationalId", "")))
            self.table.setItem(
                row, 3, QTableWidgetItem(student.get("program", "").get("name"))
            )

        self.update_total_students()

    def update_total_students(self):
        count = (
            self.session.query(func.count(Student.id))
            .filter(Student.std_no.isnot(None))
            .scalar()
        )

        self.total_label.setText(f"Registered Students: {count}")


def handle_response(student_info):
    form = StudentForm(student_info)
    form.exec()
