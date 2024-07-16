import logging
from bs4 import Tag, BeautifulSoup
import requests
from requests import Response
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from browser.payloads import create_student_payload, student_details_payload
from model import StudentInfo
from urllib.parse import quote_plus


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://cmslesothosandbox.limkokwing.net/campus/registry"


def get_form_payload(form: Tag):
    data = {}
    inputs = form.select("input")
    for tag in inputs:
        if tag.attrs['type'] == 'hidden':
            data[tag.attrs['name']] = tag.attrs['value']
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

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Browser, cls).__new__(cls)
            cls._instance.session = requests.Session()
            cls._instance.session.verify = False
        return cls._instance

    def login(self):
        logger.info("Logging in...")
        driver = webdriver.Firefox()
        logger.info(f"Fetching {self.url}...")
        driver.get(self.url)
        WebDriverWait(driver, 60 * 3).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, "[ Logout ]"))
        )
        logger.info("Logged in")

        selenium_cookies = driver.get_cookies()
        driver.quit()

        self.session.cookies.clear()
        for cookie in selenium_cookies:
            self.session.cookies.set(cookie["name"], cookie["value"], domain=cookie["domain"])

    def fetch(self, url: str) -> Response:
        logger.info(f"Fetching {url}...")
        response = self.session.get(url)
        is_logged_in = check_logged_in(response.text)
        if not is_logged_in:
            logger.info("Not logged in")
            self.login()
            response = self.session.get(url)
            logger.info(f"Logged in, re-fetching {url}...")
        if response.status_code != 200:
            logger.warning(f"Unexpected status code: {response.status_code}")
        return response

    def post(self, url: str, data: dict) -> Response:
        logger.info(f"Posting to {url}...")
        logger.info(f"Data: {data}")
        response = self.session.post(url, data)
        is_logged_in = check_logged_in(response.text)
        if not is_logged_in:
            logger.info("Not logged in")
            self.login()
            response = self.session.post(url, data)
            logger.info(f"Logged in, re-posting to {url}...")
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
            std_no = table.select_one('tr.ewTableRow td:nth-child(4)').text.strip()
            logger.info(f"Found student with student no. '{std_no}'")
        else:
            logger.warning("Student not found")
        return std_no

    def create_student(self, std: StudentInfo) -> str | None:
        url = f"{BASE_URL}/r_studentadd.php"
        std_id = self.find_student(names=std.names, national_id=std.national_id)
        if std_id:
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
        url = f"{BASE_URL}/r_stdpersonallist.php?showmaster=1&x_StudentNo={std_no}"
        self.fetch(url)
        response = self.fetch(f"{BASE_URL}/r_stdpersonaladd.php")
        page = BeautifulSoup(response.text, "lxml")
        form = page.select_one("form")
        payload = get_form_payload(form) | student_details_payload(std_no, student_info)
        response = self.post(f"{BASE_URL}/r_stdpersonaladd.php", payload)
        print(response.text)
        # if "Successful" in response.text or "Duplicate value for primary key" in response.text:
        #     logger.info("Student details added successfully")
        # else:
        #     logger.error("Failed to add student details")

    @staticmethod
    def get_search_url(names, national_id):
        base_url = f"{BASE_URL}/r_studentviewlist.php"
        params = {
            "a_search": "E",
            "z_StudentID": "=,,",
            "x_StudentID": "",
            "z_StudentName": "LIKE,'%,%'",
            "x_StudentName": quote_plus(names),
            "z_StudentNo": "LIKE,'%,%'",
            "x_StudentNo": national_id,
            "Submit": "Search"
        }

        query_string = "&".join(f"{key}={value}" for key, value in params.items())
        return f"{base_url}?{query_string}"
