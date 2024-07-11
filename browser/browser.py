import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)
BASE_URL = "https://cmslesothosandbox.limkokwing.net/campus/registry"


class Browser:
    url = f"{BASE_URL}/login.php"

    def __init__(self):
        self.driver = webdriver.Firefox()

    def login(self):
        logger.info("Logging in...")
        # driver_manager = GeckoDriverManager(cache_manager=DriverCacheManager(valid_range=30))
        # driver = webdriver.Firefox(service=GeckoService(executable_path=driver_manager.install()))
        logger.info(f"Fetching {self.url}...")
        self.driver.get(self.url)
        WebDriverWait(self.driver, 60 * 3).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, "[ Logout ]"))
        )
        # wait for 2 seconds
        time.sleep(2)
        logger.info("Logged in")

    def test(self):
        logger.info("Testing...")
        self.driver.get(f'{BASE_URL}/s_updatelist.php?showmaster=1&StudentID=901016948')
        self.driver.get(f'{BASE_URL}/s_updateadd.php')
