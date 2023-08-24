import discord
from utils.env_loader import EnvLoader
from discord.ext import commands, tasks

env_loader = EnvLoader()

# dicord bot's intents
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('!ping'):
            await message.channel.send('Pong!')

    def run(self):
        super().run(env_loader.get('DISCORD_BOT_TOKEN'), reconnect=True)
