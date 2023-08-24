import os
from dotenv import load_dotenv

class EnvLoader:
    def __init__(self):
        # load .env variables
        load_dotenv()

    def get(self, key, default=None):
        # get environment variable
        return os.getenv(key, default)
