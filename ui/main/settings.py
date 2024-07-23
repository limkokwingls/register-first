from PySide6.QtCore import QObject, QSettings, QDate


class Settings(QObject):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        super().__init__()
        self.settings = QSettings("limkokwing", "register-first")
        self.__initialized = True

    @property
    def term(self):
        return str(self.settings.value("term", ""))

    @term.setter
    def term(self, value):
        self.settings.setValue("term", value)

    @property
    def intake_date(self):
        saved_date = self.settings.value("intake_date", QDate.currentDate())
        if isinstance(saved_date, str):
            return QDate.fromString(saved_date, "yyyy-MM-dd")
        return saved_date

    def intake_date_str(self):
        return self.intake_date.toString("yyyy-MM-dd")

    @intake_date.setter
    def intake_date(self, value):
        if isinstance(value, QDate):
            value = value.toString("yyyy-MM-dd")
        self.settings.setValue("intake_date", value)

    @classmethod
    def instance(cls):
        return cls()