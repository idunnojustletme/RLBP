# load_config.py

import yaml


def load_config():
    with open("config.yaml", "r") as f:
        yaml_data = yaml.safe_load(f)
        defaults = yaml_data.get("defaults", {})
        config = yaml_data.get("config", {})
        merged_config = {**defaults, **config}
        return merged_config
