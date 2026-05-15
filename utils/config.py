import yaml
import os
from pathlib import Path

# Get the project root directory (assuming utils/config.py is 1 level down)
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / "configs" / "environment.yaml"

def load_environment_config(config_path=CONFIG_PATH):
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Config file not found: {config_path}"
        )

    with open(config_path, "r") as file:
        return yaml.safe_load(file)

# Load once when imported
settings = load_environment_config()

def get_setting(keys, default=None):
    """
    Get a setting using a dot-separated string like 'api.base_url'
    """
    keys_list = keys.split('.')
    current = settings
    for key in keys_list:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
