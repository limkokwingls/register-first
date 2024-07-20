from PySide6.QtCore import QSettings, QDate
from PySide6.QtWidgets import (QVBoxLayout, QDialog, QLineEdit,
                               QPushButton, QFormLayout, QMessageBox, QDateEdit)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("limkokwing", "register-first")
        self.setWindowTitle("Settings")
        layout = QFormLayout(self)

        self.term_input = QLineEdit(self)
        self.intake_date_input = QDateEdit(self)
        self.intake_date_input.setCalendarPopup(True)
        self.intake_date_input.setDisplayFormat("yyyy-MM-dd")

        layout.addRow("Term:", self.term_input)
        layout.addRow("Intake Date:", self.intake_date_input)

        buttons = QVBoxLayout()
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_settings)
        buttons.addWidget(save_button)

        layout.addRow(buttons)

        # Load current settings
        self.term_input.setText(str(self.settings.value("term", "")))
        saved_date = self.settings.value("intake_date", QDate.currentDate())
        if isinstance(saved_date, str):
            saved_date = QDate.fromString(saved_date, "yyyy-MM-dd")
        self.intake_date_input.setDate(saved_date)

    def save_settings(self):
        new_term = self.term_input.text()
        new_intake_date = self.intake_date_input.date().toString("yyyy-MM-dd")

        print(new_term, new_intake_date)

        self.settings.setValue("term", new_term)
        self.settings.setValue("intake_date", new_intake_date)
        self.accept()
