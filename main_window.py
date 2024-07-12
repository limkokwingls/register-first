from PySide6.QtWidgets import QMainWindow, QToolBar, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, QSpacerItem, \
    QWidget


class Header(QWidget):
    def __init__(self):
        super().__init__()
        national_id = QLineEdit()
        national_id.setPlaceholderText("National ID No.")
        reference_no = QLineEdit()
        reference_no.setPlaceholderText("Reference No.")
        button = QPushButton("Look Up")

        layout = QHBoxLayout()
        layout.addWidget(national_id)
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
