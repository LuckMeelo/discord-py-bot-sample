import json

class ConfigLoader:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config
        except FileNotFoundError:
            raise Exception(f"Config file '{self.config_path}' not found.")
        except json.JSONDecodeError:
            raise Exception(f"Error parsing config file '{self.config_path}'.")

    def get(self, key, default=None):
        return self.config.get(key, default)

