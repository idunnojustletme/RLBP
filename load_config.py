# load_config.py

import json


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)
