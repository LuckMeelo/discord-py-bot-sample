import platform, os
import discord
from utils.env_loader import EnvLoader
from utils.config_loader import ConfigLoader
from utils.logger import build_logger
from discord.ext import commands, tasks

env = EnvLoader()
config = ConfigLoader()

# dicord bot's intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config.get('prefix'), intents=intents)
        self.logger = build_logger(name=config.get('bot_name'), logfilename=config.get('log_filename'))

    async def on_ready(self):
        '''
        Print general infos about the bot and the platform its running on.
        '''
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        self.logger.info("-------------------")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('!ping'):
            await message.channel.send('Pong!')

    def run(self):
        super().run(env.get('DISCORD_BOT_TOKEN'), reconnect=True)
