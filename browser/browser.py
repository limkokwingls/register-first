import logging
from urllib.parse import quote_plus

import requests
import urllib3
from bs4 import BeautifulSoup, Tag
from requests import Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from urllib3.exceptions import InsecureRequestWarning

from browser.payloads import create_student_payload, student_details_payload, register_program_payload, \
    add_semester_payload, add_update_payload
from model import StudentInfo, Program
from ui.main.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()

BASE_URL = f"{settings.base_url}campus/registry"

urllib3.disable_warnings(InsecureRequestWarning)


def get_form_payload(form: Tag):
    data = {}
    inputs = form.select("input")
    for tag in inputs:
        if tag.attrs["type"] == "hidden":
            data[tag.attrs["name"]] = tag.attrs["value"]
    return data


def check_logged_in(html: str) -> bool:
    page = BeautifulSoup(html, "lxml")
    form = page.select_one("form")
    if form:
        if form.attrs.get("action") == "login.php":
            return False
    return True


class Browser:
    _instance = None
    url = f"{BASE_URL}/login.php"
    logged_in = False
    session: requests.Session | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Browser, cls).__new__(cls)
            cls._instance.session = requests.Session()
            cls._instance.session.verify = False
        return cls._instance

    def login(self):
        logger.info("Logging in...")
        driver = webdriver.Firefox()
        logger.info(f"Fetching {self.url}")
        driver.get(self.url)
        WebDriverWait(driver, 60 * 3).until(
            expected_conditions.presence_of_element_located(
                (By.LINK_TEXT, "[ Logout ]")
            )
        )
        logger.info("Logged in")

        selenium_cookies = driver.get_cookies()
        driver.quit()

        self.session.cookies.clear()
        for cookie in selenium_cookies:
            self.session.cookies.set(
                cookie["name"], cookie["value"], domain=cookie["domain"]
            )

    def fetch(self, url: str) -> Response:
        logger.info(f"Fetching {url}")
        response = self.session.get(url, timeout=120)
        is_logged_in = check_logged_in(response.text)
        if not is_logged_in:
            logger.info("Not logged in")
            self.login()
            logger.info(f"Logged in, re-fetching {url}")
            response = self.session.get(url, timeout=120)
        if response.status_code != 200:
            logger.warning(f"Unexpected status code: {response.status_code}")
        return response

    def post(self, url: str, data: dict | str) -> Response:
        logger.info(f"Posting to {url}")
        logger.info(f"Data: {data}")
        response = self.session.post(url, data, timeout=120)
        is_logged_in = check_logged_in(response.text)
        if not is_logged_in:
            logger.info("Not logged in")
            self.login()
            logger.info(f"Logged in, re-posting to {url}")
            response = self.session.post(url, data, timeout=120)
        if response.status_code != 200:
            logger.warning(f"Unexpected status code: {response.status_code}")
        return response

    def find_student(self, national_id: str, names: str) -> str | None:
        logger.info(f"Searching for student with national id '{national_id}'")
        url = self.get_search_url(names=names, national_id=national_id)
        response = self.fetch(url)
        page = BeautifulSoup(response.text, "lxml")
        table = page.select_one("table#ewlistmain")
        std_no = None
        if table:
            std_no = table.select_one("tr.ewTableRow td:nth-child(4)").text.strip()
            logger.info(f"Found student with student no. '{std_no}'")
        else:
            logger.warning("Student not found")
        return std_no

    def check_logged_in(self):
        url = f"{BASE_URL}/r_studentviewlist.php"
        self.fetch(url)

    def create_student(self, std: StudentInfo) -> str | None:
        logger.info("Creating student...")
        url = f"{BASE_URL}/r_studentadd.php"
        std_id = self.find_student(names=std.names, national_id=std.national_id)
        if std_id:
            logger.info(f"Student already exists, student number: {std_id}")
            return std_id
        response = self.fetch(url)
        page = BeautifulSoup(response.text, "lxml")
        form = page.select_one("form")
        payload = get_form_payload(form) | create_student_payload(std)
        response = self.post(url, payload)
        if "Successful" in response.text:
            logger.info("Student created successfully")
            return self.find_student(std.national_id, std.names)
        else:
            logger.error("Failed to create student")
            return None

    def add_student_details(self, std_no: str, student_info: StudentInfo):
        logger.info(f"Adding student details for '{std_no}'")
        url = f"{BASE_URL}/r_stdpersonallist.php?showmaster=1&x_StudentNo={std_no}"
        self.fetch(url)
        response = self.fetch(f"{BASE_URL}/r_stdpersonaladd.php")
        page = BeautifulSoup(response.text, "lxml")
        form = page.select_one("form")
        payload = get_form_payload(form) | student_details_payload(std_no, student_info)
        response = self.post(f"{BASE_URL}/r_stdpersonaladd.php", payload)
        if ("Successful" in response.text
                or "Duplicate value for primary key" in response.text):
            logger.info("Student details added successfully")
            return True
        else:
            logger.error("Failed to add student details")
            return False

    def register_program(self, std_no: str, program_code: str) -> int | None:
        logger.info(f"Registering student '{std_no}' into program '{program_code}'")
        url = f"{BASE_URL}/r_stdprogramlist.php?showmaster=1&StudentID={std_no}"
        std_program_id = self.get_std_program_id(self.fetch(url), program_code)
        if std_program_id:
            logger.info(
                f"Student already registered into program '{program_code}', student program id: {std_program_id}")
            return int(std_program_id.strip())
        response = self.fetch(f"{BASE_URL}/r_stdprogramadd.php")
        page = BeautifulSoup(response.text, "lxml")
        form = page.select_one("form")
        payload = get_form_payload(form) | register_program_payload(std_no, program_code)
        response = self.post(f"{BASE_URL}/r_stdprogramadd.php", payload)
        std_program_id = self.get_std_program_id(response, program_code)
        if "Successful" in response.text:
            logger.info(f"Student registered into program successfully, student program id: {std_program_id}")
            return int(std_program_id.strip())
        else:
            logger.error("Failed to register student into program")

    def add_semester(self, std_program_id: int, program_code: str, std: StudentInfo) -> int | None:
        logger.info(f"Adding semester for student '{std_program_id}'")
        url = f"{BASE_URL}/r_stdsemesterlist.php?showmaster=1&StdProgramID={std_program_id}"
        term = Settings().term
        std_semester_id = self.get_id_for(self.fetch(url), term)
        if std_semester_id:
            logger.info(f"Semester already added, semester id: {std_semester_id}")
            return int(std_semester_id.strip())
        response = self.fetch(f"{BASE_URL}/r_stdsemesteradd.php")
        page = BeautifulSoup(response.text, "lxml")
        form = page.select_one("form")
        payload = (get_form_payload(form) |
                   add_semester_payload(std_program_id=std_program_id,
                                        semester_id=self.read_semester_id(form, std.program),
                                        program_code=program_code, term=term))
        response = self.post(f"{BASE_URL}/r_stdsemesteradd.php", payload)
        std_semester_id = self.get_id_for(response, term)
        if "Successful" in response.text:
            logger.info(f"Semester added successfully, semester id: {std_semester_id}")
            return int(std_semester_id.strip())
        else:
            logger.error("Failed to add semester")

    def add_modules(self, std_semester_id: int):
        url = f"{BASE_URL}/r_stdmodulelist.php?showmaster=1&StdSemesterID={std_semester_id}"
        self.fetch(url)
        add_response = self.fetch(f"{BASE_URL}/r_stdmoduleadd1.php")
        page = BeautifulSoup(add_response.text, "lxml")
        checkboxes = page.find_all('input', type='checkbox')

        modules = []
        for i, checkbox in enumerate(checkboxes):
            parent_tr = checkbox.find_parent('tr')
            # is_disabled = 'disabled' in checkbox.attrs
            is_blue = parent_tr and 'phpmaker1' in parent_tr.get('class', [])

            if is_blue:
                modules.append(checkbox.attrs['value'])

        modules_with_amounts = []
        for module in modules:
            parts = module.split('-')
            parts[-1] = '1200'
            modules_with_amounts.append('-'.join(parts))

        payload = get_form_payload(page) | {
            "Submit": "Add+Modules",
            "take[]": modules_with_amounts
        }
        hidden_inputs = page.find_all('input', type='hidden')
        for hidden in hidden_inputs:
            payload.update({hidden['name']: hidden['value']})

        self.post(f"{BASE_URL}/r_stdmoduleadd1.php", payload)

    def add_update(self, std_no: str):
        page = BeautifulSoup(self.fetch(f"{BASE_URL}/s_updateadd.php").text, "lxml")
        form = page.select_one("form")
        payload = get_form_payload(form) | add_update_payload(std_no)
        self.post(f"{BASE_URL}/s_updateadd.php", payload)

    @staticmethod
    def read_semester_id(form: Tag, program: Program):
        target = "Year 1 Sem 1"
        if program.bhr_year:
            target = program.bhr_year
        sem_options = form.select("#x_SemesterID option")
        for option in sem_options:
            option_str = option.get_text(strip=True)
            if target in option_str:
                return option.attrs['value']

        raise ValueError(
            f"semester_id cannot be empty was expecting 'Year 1 Sem 1' but not found")

    @staticmethod
    def get_id_for(response: requests.Response, search_key: str) -> str:
        page = BeautifulSoup(response.text, "lxml")
        table = page.select_one("table#ewlistmain")
        if table:
            rows = table.select("tr.ewTableRow")
            for row in rows:
                cols = row.select("td")
                if search_key in cols[0].text.strip():
                    return row.select_one("a").attrs["href"].split("=")[-1]

    @staticmethod
    def get_std_program_id(response: requests.Response, code: str) -> str:
        page = BeautifulSoup(response.text, "lxml")
        table = page.select_one("table#ewlistmain")
        if table:
            rows = table.select("tr.ewTableRow")
            for row in rows:
                cols = row.select("td")
                code_text = cols[0].text.strip()
                status = cols[4].text.strip()
                logger.info(f"Searching for {code}, Found (Code: {code_text}, Status: {status})")
                if code_text.startswith(code) and status == "Active":
                    return row.select_one("a").attrs["href"].split("=")[-1]

    @staticmethod
    def get_search_url(names, national_id):
        base_url = f"{BASE_URL}/r_studentviewlist.php"
        params = {
            "a_search": "E",
            "z_StudentID": "=,,",
            "x_StudentID": "",
            "z_StudentName": "LIKE%2C%27%25%2C%25%27",
            "x_StudentName": quote_plus(names),
            "z_StudentNo": "LIKE,'%,%'",
            "x_StudentNo": national_id,
            "Submit": "Search",
        }

        query_string = "&".join(f"{key}={value}" for key, value in params.items())
        return f"{base_url}?{query_string}"
