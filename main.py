import firebase_admin
from PySide6.QtWidgets import QApplication
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1 import FieldFilter

from config.firebase import db
from main_window import MainWindow



def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
