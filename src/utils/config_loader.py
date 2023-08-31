import json


class ConfigLoader:
    def __init__(self, config_path='config.json'):
        # Initialize the ConfigLoader with the specified config file path
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        '''
        Load the configuration variables from the specified config file.
        '''
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config
        except FileNotFoundError:
            raise Exception(f"Config file '{self.config_path}' not found.")
        except json.JSONDecodeError:
            raise Exception(f"Error parsing config file '{self.config_path}'.")

    def get(self, key, default=None):
        '''
        Get the value of a configuration variable using its key.

        :param key: The key of the configuration variable.
        :param default: The default value to return if the variable is not set.
        :return: The value of the configuration variable or the default value if not set.
        '''
        return self.config.get(key, default)
