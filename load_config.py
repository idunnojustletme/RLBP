# load_config.py

import yaml


def load_config():
    with open("config.yaml", "r") as f:
        yaml_data = yaml.safe_load(f)
        config = yaml_data.get("config", {})
        return config
