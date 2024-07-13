from PySide6.QtWidgets import (QMainWindow, QWidgetAction, QToolBar, QVBoxLayout, QLineEdit, QHBoxLayout,
                               QPushButton, QSpacerItem, QWidget, QTableWidget, QSizePolicy, QLabel, QHeaderView)
from PySide6.QtGui import QPageSize
from PySide6.Qt3DCore import QIntList


class InputField(QWidget):
    def __init__(self, label: str):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.label = QLabel(label)
        self.input = QLineEdit()
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.input)


class Header(QWidget):
    def __init__(self):
        super().__init__()
        id_input = InputField("National Id")
        reference_no = InputField("Reference No.")
        button = QPushButton("Look Up")

        layout = QHBoxLayout()
        layout.addWidget(id_input)
        layout.addWidget(reference_no)
        layout.addWidget(button)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        header = Header()
        layout = QVBoxLayout()
        layout.addWidget(header)
        central = QWidget()
        central.setLayout(layout)

        self.setCentralWidget(central)
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Student No.", "Name", "National ID", "Program"])
        layout.addWidget(table)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.resize(800, 500)
