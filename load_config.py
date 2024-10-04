# load_config.py

import yaml


def load_config():
    with open("config.yaml", "r") as f:
        yaml_data = yaml.safe_load(f)
        config = yaml_data.get("config", {})

        # Define default config values
        default_config = {
            "intiface_ip": "ws://127.0.0.1:12345",
            "min_vibe_strength": 20,
            "max_vibe_strength": 100,
            "min_vibe_time": 0.5,
            "max_vibe_time": 20.0,
            "vibe_strength_divider": 1.5,
            "vibe_time_divider": 25,
            "min_vibe_score": 10,
        }

        # Validate config value types
        validated_config = {}
        for key, value in config.items():
            if key not in default_config:
                raise ValueError(f"Unknown config key: '{key}'")
            if not isinstance(value, type(default_config[key])):
                print(
                    f"Warning: Invalid {key} value: '{value}' (expected {type(default_config[key]).__name__}). Using default value"
                )
                validated_config[key] = default_config[key]
            else:
                validated_config[key] = value

        # Add missing default config values
        for key, value in default_config.items():
            if key not in validated_config:
                validated_config[key] = value

        # Check that intiface_ip starts with ws://
        for key, value in validated_config.items():
            if key == "intiface_ip" and not value.startswith("ws://"):
                print(
                    f"Warning: Invalid intiface_ip value: '{value}' (expected to start with ws://). Using default value"
                )
        return validated_config
