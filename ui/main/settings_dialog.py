from PySide6.QtCore import QObject, QSettings, QDate
from PySide6.QtWidgets import (QVBoxLayout, QDialog, QLineEdit,
                               QPushButton, QFormLayout, QMessageBox, QDateEdit)

from ui.main.settings import Settings


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = Settings()
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
        self.term_input.setText(self.settings.term)
        self.intake_date_input.setDate(self.settings.intake_date)

    def save_settings(self):
        new_term = self.term_input.text()
        new_intake_date = self.intake_date_input.date()

        self.settings.term = new_term
        self.settings.intake_date = new_intake_date
        self.accept()

# Example usage in other parts of your application:
# settings_manager = SettingsManager()
# current_term = settings_manager.term
# current_intake_date = settings_manager.intake_date
