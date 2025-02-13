from PySide6.QtWidgets import QApplication
from sqlalchemy.orm import sessionmaker

from config.database import engine
from models import Base
from ui.main.main_window import MainWindow
from ui.main.settings import Settings
from ui.main.settings_dialog import SettingsDialog

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def main():
    app = QApplication()
    window = MainWindow(get_db())
    window.show()
    settings = Settings()
    if settings.term == "" or not settings.intake_date or settings.base_url == "":
        dialog = SettingsDialog(window)
        dialog.exec()
    app.exec()


if __name__ == "__main__":
    main()
