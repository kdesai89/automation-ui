from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from core.logger import get_logger

log = get_logger("base_page")


class BasePage:
    def __init__(self, driver, timeout_sec: int):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout_sec)

    def open(self, url: str):
        log.info(f"Opening URL: {url}")
        self.driver.get(url)

    def click(self, locator):
     log.info(f"Clicking element: {locator}")
     try:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
     except TimeoutException:
        log.error(f"Timeout waiting for clickable: {locator}")
        raise

    def type(self, locator, text: str, clear: bool = True):
     log.info(f"Typing into: {locator} | value_length={len(text)}")
     try:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        element.send_keys(text)
     except TimeoutException:
        log.error(f"Timeout waiting for visible: {locator}")
        raise

    def is_visible(self, locator) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
