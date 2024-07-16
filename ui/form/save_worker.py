from PySide6.QtCore import QObject, Slot, Signal

from browser import Browser


class SaveWorker(QObject):
    finished = Signal(bool, str)
    progress = Signal(str)

    def __init__(self, student):
        super().__init__()
        self.student = student

    @Slot()
    def save(self):
        try:
            self.progress.emit("Initializing...")
            browser = Browser()
            browser.check_logged_in()
            self.progress.emit("Creating student...")
            std_no = browser.create_student(self.student)

            if std_no:
                self.progress.emit(f"Student created! '{std_no}', adding details...")
                browser.add_student_details(std_no, self.student)
                self.finished.emit(True, std_no)
            else:
                self.finished.emit(False, "Failed to create student")
        except Exception as e:
            self.finished.emit(False, str(e))