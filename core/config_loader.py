import os
import yaml
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class EnvConfig:
    name: str
    base_url: str
    timeout_sec: int


@dataclass
class Settings:
    browser: str
    headless: bool
    implicit_wait_sec: int
    page_load_timeout_sec: int


class ConfigLoader:
    @staticmethod
    def _load_yaml(relative_path: str) -> dict:
        path = ROOT / relative_path
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    @staticmethod
    def load_env(override_env: str | None = None) -> EnvConfig:
        raw = ConfigLoader._load_yaml("config/environments.yaml")

        # Priority: CLI override > ENV var > default 'qa'
        env_name = override_env or os.getenv("TEST_ENV") or "qa"

        if env_name not in raw:
            raise KeyError(
                f"Env '{env_name}' not found in config/environments.yaml. "
                f"Available: {list(raw.keys())}"
            )

        block = raw[env_name]
        return EnvConfig(
            name=env_name,
            base_url=str(block["base_url"]).rstrip("/"),
            timeout_sec=int(block.get("timeout_sec", 20)),
        )

    @staticmethod
    def load_settings() -> Settings:
        raw = ConfigLoader._load_yaml("config/settings.yaml")

        return Settings(
            browser=str(raw.get("browser", "chrome")).lower(),
            headless=bool(raw.get("headless", False)),
            implicit_wait_sec=int(raw.get("implicit_wait_sec", 0)),
            page_load_timeout_sec=int(raw.get("page_load_timeout_sec", 60)),
        )
