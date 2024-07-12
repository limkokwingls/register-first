import logging

import requests
from requests import Response
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# from webdriver_manager.core.driver_cache import DriverCacheManager
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager

logger = logging.getLogger(__name__)
BASE_URL = "https://cmslesothosandbox.limkokwing.net/campus/registry"


class Browser:
    url = f"{BASE_URL}/login.php"

    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False

    def login(self):
        logger.info("Logging in...")
        # driver_manager = GeckoDriverManager(cache_manager=DriverCacheManager(valid_range=30))
        # driver = webdriver.Firefox(service=GeckoService(executable_path=driver_manager.install()))
        driver = webdriver.Firefox()
        logger.info(f"Fetching {self.url}...")
        driver.get(self.url)
        WebDriverWait(driver, 60 * 3).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, "[ Logout ]"))
        )
        logger.info("Logged in")

        cookies = driver.get_cookies()
        driver.quit()

        for cookie in cookies:
            self.session.cookies.set(cookie["name"], cookie["value"])

    def fetch(self, url: str) -> Response:
        logger.info(f"Fetching {url}...")
        response = self.session.get(url)
        if response.status_code != 200:
            self.session.cookies = response.cookies
        return response
