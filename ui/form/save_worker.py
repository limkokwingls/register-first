import logging
import traceback

from PySide6.QtCore import QObject, Slot, Signal

from browser import Browser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SaveWorker(QObject):
    finished = Signal(bool, str)
    message = Signal(str)
    progress = Signal(int)

    def __init__(self, student):
        super().__init__()
        self.student = student

    @Slot()
    def save(self):
        try:
            self.progress.emit(0)
            self.message.emit("Initializing...")
            browser = Browser()
            browser.check_logged_in()
            self.message.emit("Creating student...")
            self.progress.emit(2)
            std_no = browser.create_student(self.student)

            if std_no:
                self.progress.emit(3)
                self.message.emit(f"Adding student details, student number: {std_no}...")
                success = browser.add_student_details(std_no, self.student)
                if success:
                    self.progress.emit(4)
                    self.message.emit(f"Registering for {self.student.program.name}...")
                    std_program_id = browser.register_program(std_no, self.student.program.code)
                    if std_program_id:
                        self.progress.emit(5)
                        self.message.emit(f"Adding semester...")
                        std_semester_id = browser.add_semester(std_program_id, self.student.program.code)
                        if std_semester_id:
                            self.progress.emit(6)
                            self.message.emit("Adding modules...")
                            browser.add_modules(std_semester_id)
                            self.progress.emit(7)
                            self.message.emit("Updating semester registration...")
                            browser.add_update(std_no)
                            self.progress.emit(8)
                        else:
                            self.message.emit("Failed to add semester")

                self.finished.emit(True, std_no)
            else:
                self.finished.emit(False, "Failed to create student")
        except Exception as e:
            logger.error(f"Error saving student: {e}")
            traceback.print_exc()
            self.finished.emit(False, str(e))
