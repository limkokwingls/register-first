from PySide6 import QtGui
from PySide6.QtWidgets import (QMainWindow, QWidgetAction, QToolBar, QVBoxLayout, QLineEdit, QHBoxLayout,
                               QPushButton, QSpacerItem, QWidget, QTableWidget, QSizePolicy, QLabel, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.Qt3DCore import QIntList

from ui.main.LookupWidget import LookupWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        lookup = LookupWidget()

        layout = QVBoxLayout()
        layout.addWidget(lookup)
        central = QWidget()
        central.setLayout(layout)

        self.setCentralWidget(central)
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Student No.", "Name", "National ID", "Program"])
        layout.addWidget(table)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.resize(800, 500)
