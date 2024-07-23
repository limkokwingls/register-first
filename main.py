from PySide6.QtWidgets import QApplication

from ui.main.main_window import MainWindow
from ui.main.settings import Settings
from ui.main.settings_dialog import SettingsDialog


def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    settings = Settings()
    if settings.term == "" or not settings.intake_date or settings.base_url == "":
        dialog = SettingsDialog(window)
        dialog.exec()
    app.exec()


if __name__ == "__main__":
    main()
