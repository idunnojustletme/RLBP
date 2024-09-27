# load_config.py

import yaml


def load_config(self):
    self.gui.print("Loading config.yaml file")
    with open("config.yaml", "r") as f:
        yaml_data = yaml.safe_load(f)
        defaults = yaml_data.get("defaults", {})
        config = yaml_data.get("config", {})
        merged_config = {**defaults, **config}
        return merged_config


# FIXME TESTING ONLY
if __name__ == "__main__":
    for key, value in load_config().items():
        print(f"{key}: {value}")
