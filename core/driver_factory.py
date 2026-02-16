# core/driver_factory.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


class DriverFactory:
    @staticmethod
    def create(browser: str, headless: bool):
        browser = (browser or "chrome").lower()

        if browser == "chrome":
            options = ChromeOptions()

            if headless:
                # new headless mode is more stable on newer Chrome
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--disable-gpu")
            else:
                options.add_argument("--start-maximized")

            # enterprise stability defaults (Docker/CI safe)
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-infobars")
            options.add_argument("--remote-allow-origins=*")

            # optional: reduces some automation banner / detection issues
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            driver = webdriver.Chrome(options=options)
            return driver

        raise ValueError(f"Unsupported browser: {browser}")
