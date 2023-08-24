import platform, os
import asyncio

import discord
from discord.ext import commands, tasks

import utils.embeds as embeds
from utils.env_loader import EnvLoader
from utils.config_loader import ConfigLoader
from utils.logger import build_logger


EXTENSIONS = [
    "bot.commands.ping",
]

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
        asyncio.run(self._load_cogs())

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
        '''
        Process every messages sent by users and trigger the appropriate
        command.
        '''
        if message.author == self.user:
            return
        await self.process_commands(message)
    
    async def on_command_completion(self, context: commands.Context) -> None:
        '''
        The code in this event is executed every time a normal command has been *successfully* executed.
        '''
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])

        if context.guild is not None:
            self.logger.info(f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
        else:
            self.logger.info(f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")
    
    async def on_command_error(self, context: commands.Context, error) -> None:
        '''
        The code in this event is executed every time a normal valid command catches an error.
        '''
        if isinstance(error, commands.CommandNotFound):
            self.logger.warning(f"Command not found: {context.message.content} by {context.author} (ID: {context.author.id})")

        elif isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = embeds.embed_error(
                description=f"**Please slow down** - You can use this command again in \
                    {f'{round(hours)} hours' if round(hours) > 0 else ''} \
                        {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} \
                            {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = embeds.embed_error(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = embeds.embed_error(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = embeds.embed_error(
                # We need to capitalize because the command arguments have no capital letter in the code.
                description=str(error).capitalize(),
            )
            await context.send(embed=embed)

        else:
            raise error

    async def _load_cogs(self):
        for extension in EXTENSIONS:
            await self.load_extension(extension)
    
    def run(self):
        super().run(env.get('DISCORD_BOT_TOKEN'), reconnect=True)

    