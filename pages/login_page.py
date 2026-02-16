from core.base_page import BasePage
from locators.login_locators import LoginLocators

class LoginPage(BasePage):
    def login(self, username: str, password: str):
        self.type(LoginLocators.USERNAME, username)
        self.type(LoginLocators.PASSWORD, password)
        self.click(LoginLocators.BTN_LOGIN)

    def has_error(self) -> bool:
        return self.is_visible(LoginLocators.ERROR_MSG)
