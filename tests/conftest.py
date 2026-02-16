# tests/conftest.py
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest
from core.config_loader import ConfigLoader
from core.driver_factory import DriverFactory
from core.data_loader import DataLoader
from core.logger import get_logger

log = get_logger("pytest")

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa", help="qa|stage|prod")
    parser.addoption("--browser", action="store", default="chrome", help="chrome")
    parser.addoption("--headless", action="store_true", default=False, help="Run headless")
    parser.addoption("--role", action="store", default="admin", help="admin|user|...")

@pytest.fixture(scope="session")
def env_name(request) -> str:
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def role(request) -> str:
    return request.config.getoption("--role")

@pytest.fixture(scope="session")
def env(env_name):
    e = ConfigLoader.load_env(env_name)
    setattr(e, "name", env_name)  # so tests can use env.name
    return e

@pytest.fixture(scope="session")
def settings(request):
    s = ConfigLoader.load_settings()

    s.browser = request.config.getoption("--browser") or s.browser

    # Headless priority:
    # 1) CLI flag --headless
    # 2) ENV var HEADLESS=true/1/yes
    # 3) settings.yaml default
    cli_headless = bool(request.config.getoption("--headless"))

    headless_env_raw = os.getenv("HEADLESS")
    env_headless = (
        str(headless_env_raw).strip().lower() in ("1", "true", "yes", "y")
        if headless_env_raw is not None
        else False
    )

    if cli_headless:
        s.headless = True
    elif headless_env_raw is not None:
        s.headless = env_headless
    # else: keep s.headless from settings.yaml

    return s

@pytest.fixture(scope="session")
def data():
    return DataLoader.load_data()

@pytest.fixture
def driver(settings):
    drv = DriverFactory.create(settings.browser, settings.headless)
    drv.implicitly_wait(getattr(settings, "implicit_wait_sec", 0))
    drv.set_page_load_timeout(getattr(settings, "page_load_timeout_sec", 60))
    yield drv
    drv.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver", None)
        if drv:
            Path("reports").mkdir(exist_ok=True)

            png = Path("reports") / f"{item.name}.png"
            drv.save_screenshot(str(png))

            html = Path("reports") / f"{item.name}.html"
            try:
                html.write_text(drv.page_source, encoding="utf-8")
            except Exception:
                pass

            url_txt = Path("reports") / f"{item.name}.url.txt"
            try:
                url_txt.write_text(drv.current_url, encoding="utf-8")
            except Exception:
                pass

            log.error(f"Saved artifacts: {png}, {html}, {url_txt}")
