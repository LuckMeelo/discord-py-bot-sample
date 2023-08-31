import os
from dotenv import load_dotenv


class EnvLoader:
    '''
    Custom class to get environment variables loading .env
    '''

    def __init__(self):
        # Load environment variables from the .env file
        load_dotenv()

    def get(self, key, default=None):
        '''
        Get the value of an environment variable from its key.

        :param key: The key of the environment variable.
        :param default: The default value to return if the variable is not set.
        :return: The value of the environment variable or the default value if not set.
        '''
        return os.getenv(key, default)
