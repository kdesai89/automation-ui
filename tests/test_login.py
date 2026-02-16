import pytest
from pages.login_page import LoginPage
from core.data_loader import DataLoader


@pytest.mark.smoke
def test_login_admin(driver, env, data):
    page = LoginPage(driver, timeout_sec=env.timeout_sec)
    page.open(env.base_url)

    admin = DataLoader.get_user(data, env.name, "admin")
    page.login(admin["username"], admin["password"])

    # Minimal real assertion (stable for CI)
    assert driver.current_url != env.base_url, "Login likely failed: URL did not change after login."
