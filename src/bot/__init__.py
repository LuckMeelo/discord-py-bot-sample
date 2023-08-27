import platform
import os
import asyncio

import discord
from discord.ext import commands, tasks

# Importing components from the project
from utils.env_loader import EnvLoader
from utils.config_loader import ConfigLoader
from utils.logger import build_logger

# List of extensions (cogs) to load
EXTENSIONS = [
    # modules
    "bot.cogs.general",
    "bot.cogs.sample",
    # events
    "bot.cogs.events.command_events",
    "bot.cogs.events.message_events",
]

# Load environment variables
env = EnvLoader()

# Load configuration from config.json
config = ConfigLoader()

# Set up bot intents
intents = discord.Intents.default()
intents.guilds = True  # Enable guild-related events
intents.members = True  # Allow receiving events related to members
intents.message_content = True

# Subclassing commands.Bot to customize bot behavior
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config.get('prefix'), intents=intents)
        # Adding config and a logger
        self.config = config
        self.logger = build_logger(name=config.get('bot_name'), logfilename=config.get('log_filename'))
        # Remove help command to add our custom one
        self.remove_command('help')
        # Adding all cogs
        asyncio.run(self._load_cogs())

    async def on_ready(self):
        '''
        Event handler: Called when the bot is ready.
        '''
        # Print general information about the bot and the platform it's running on
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        self.logger.info("-------------------")
    
    async def _load_cogs(self):
        '''
        Load all cogs (extensions) into the bot.
        '''
        for extension in EXTENSIONS:
            await self.load_extension(extension)

    def run(self):
        '''
        Run the bot using the token from environment variables.
        '''
        super().run(env.get('DISCORD_BOT_TOKEN'), reconnect=True)
