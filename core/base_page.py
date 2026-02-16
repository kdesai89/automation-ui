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
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type(self, locator, text: str, clear: bool = True):
        log.info(f"Typing into: {locator} | value_length={len(text)}")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        element.send_keys(text)

    def is_visible(self, locator) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
