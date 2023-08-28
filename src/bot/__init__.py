import platform
import os
import asyncio

import discord
from discord.ext import commands, tasks

# Importing components from the project
from utils.env_loader import EnvLoader
from utils.config_loader import ConfigLoader
from utils.logger import build_logger
import utils.embeds as embeds

# List of extensions (cogs) to load
EXTENSIONS = [
    # modules
    "bot.cogs.general",
    "bot.cogs.hello"
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
    
    # Cog event: Called when a message is sent
    async def on_message(self, message):
        '''
        Process every messages sent by users and trigger the appropriate command.
        '''
        # Avoid processing the bot's own messages
        if message.author == self.user or message.author.bot:
            return
        # Process commands in the message content
        await self.process_commands(message)
    
     # Cog event: Called when a command is successfully executed
    async def on_command_completion(self, context: commands.Context) -> None:
        '''
        This event is executed every time a normal command has been *successfully* executed.
        '''
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])

        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")

    # Cog event: Called when a command catches an error
    async def on_command_error(self, context: commands.Context, error) -> None:
        '''
        This event is executed every time a normal valid command catches an error.
        '''
        # Handle different types of errors
        if isinstance(error, commands.CommandNotFound):
            self.logger.warning(
                f"Command not found: {context.message.content} by {context.author} (ID: {context.author.id})")
            embed = embeds.error_embed(
                desc="You are missing the permission(s) `"
                + "` to execute this command!",
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.CommandOnCooldown):
            # Calculate the cooldown in hours, minutes, and seconds
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            
            # Create and send an error embed
            embed = embeds.error_embed(
                desc=f"**Please slow down** - You can use this command again in \
                    {f'{round(hours)} hours' if round(hours) > 0 else ''} \
                        {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} \
                            {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            # Create and send an error embed for missing permissions
            embed = embeds.error_embed(
                desc="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = embeds.error_embed(
                desc="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = embeds.error_embed(
                # We need to capitalize because the command arguments have no capital letter in the code.
                desc=str(error).capitalize(),
            )
            await context.send(embed=embed)

        # ... (other error cases)
        
        else:
            raise error
