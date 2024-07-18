import firebase_admin
from PySide6.QtWidgets import QApplication
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1 import FieldFilter

from browser import Browser
from config.firebase import db
from main_window import MainWindow


def main():
    # app = QApplication()
    # window = MainWindow()
    # window.show()
    # app.exec()

    browser = Browser()
    browser.add_modules(97067)


if __name__ == "__main__":
    main()
