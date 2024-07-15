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

from browser.payloads import create_student_payload
from model import StudentInfo
from program_codes import get_program

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
    return form is None or form.attrs["action"] != "login.php"


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

    def create_student(self, student_info: StudentInfo) -> bool:
        url = f"{BASE_URL}/r_studentadd.php"
        response = self.fetch(url)
        page = BeautifulSoup(response.text, "lxml")
        form = page.select_one("form")
        payload = get_form_payload(form) | create_student_payload(student_info)
        response = self.post(url, payload)
        if "Successful" in response.text:
            logger.info("Student created successfully")
            return True
        else:
            logger.error("Failed to create student")
            return False
