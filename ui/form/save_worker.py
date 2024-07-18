import logging
import traceback

from PySide6.QtCore import QObject, Slot, Signal

from browser import Browser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
                self.progress.emit(f"Adding student details, student number: {std_no}...")
                success = browser.add_student_details(std_no, self.student)
                if success:
                    self.progress.emit(f"Registering for {self.student.program.name}...")
                    std_program_id = browser.register_program(std_no, self.student.program.code)
                    if std_program_id:
                        self.progress.emit(f"Adding semester...")
                        std_semester_id = browser.add_semester(std_program_id, self.student.program.code)
                        if std_semester_id:
                            self.progress.emit("Adding modules...")
                            browser.add_modules(std_semester_id)
                            self.progress.emit("Updating semester registration...")
                            browser.add_update(std_no)
                        else:
                            self.progress.emit("Failed to add semester")


                self.finished.emit(True, std_no)
            else:
                self.finished.emit(False, "Failed to create student")
        except Exception as e:
            logger.error(f"Error saving student: {e}")
            traceback.print_exc()
            self.finished.emit(False, str(e))
