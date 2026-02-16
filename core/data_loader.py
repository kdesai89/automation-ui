# core/data_loader.py
import yaml
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]

class DataLoader:
    @staticmethod
    def load_yaml(relative_path: str) -> Dict[str, Any]:
        path = ROOT / relative_path
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    @staticmethod
    def load_data() -> Dict[str, Any]:
        return DataLoader.load_yaml("data/data.yaml")

    @staticmethod
    def get_user(data: Dict[str, Any], env_name: str, role: str) -> Dict[str, str]:
        env_block = data.get(env_name)
        if not env_block:
            raise KeyError(f"Env '{env_name}' not found in data.yaml")

        user = env_block.get("users", {}).get(role)
        if not user:
            raise KeyError(f"Role '{role}' not found under {env_name}.users")

        username = user.get("username")
        password = user.get("password")

        if not username:
            raise ValueError(f"Missing username for {env_name}.users.{role}")
        if password is None or password == "":
            raise ValueError(f"Missing password for {env_name}.users.{role}")

        return {"username": username, "password": password}
