from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout


class InputField(QWidget):
    def __init__(self, label: str):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.label = QLabel(label)
        self.input = QLineEdit()
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.input)


class LookupWidget(QWidget):
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