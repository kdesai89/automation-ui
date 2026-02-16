from selenium.webdriver.common.by import By

class LoginLocators:
    USERNAME = (By.ID, "userName")
    PASSWORD = (By.ID, "password")
    BTN_LOGIN = (By.ID, "login")
    ERROR_MSG = (By.XPATH, "//div[contains(@class,'validation-summary-errors')]//li")
