from PySide6.QtCore import QObject, QSettings, QDate, QUrl
from PySide6.QtWidgets import (QVBoxLayout, QDialog, QLineEdit,
                               QPushButton, QFormLayout, QMessageBox, QDateEdit, QWidget, QSizePolicy)

from ui.main.settings import Settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = Settings()
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 200)
        layout = QFormLayout(self)
        layout.setContentsMargins(20, 30, 20, 20)
        layout.setSpacing(10)

        self.term_input = QLineEdit(self)
        self.intake_date_input = QDateEdit(self)
        self.intake_date_input.setCalendarPopup(True)
        self.intake_date_input.setDisplayFormat("yyyy-MM-dd")
        self.base_url = QLineEdit(self)

        layout.addRow("Term:", self.term_input)
        layout.addRow("Intake Date:", self.intake_date_input)
        layout.addRow("Base URL:", self.base_url)

        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addRow(spacer)

        buttons = QVBoxLayout()
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_settings)
        buttons.addWidget(save_button)

        layout.addRow(buttons)

        # Load current settings
        self.term_input.setText(self.settings.term)
        self.intake_date_input.setDate(self.settings.intake_date)
        self.base_url.setText(self.settings.base_url)

    def save_settings(self):
        new_term = self.term_input.text()
        new_intake_date = self.intake_date_input.date()

        self.settings.term = new_term
        self.settings.intake_date = new_intake_date
        self.settings.base_url = self.base_url.text()
        self.accept()