import discord
from discord.ext import commands

import utils.embeds as embeds  # Import utility for embeds

# Defining the MessageEvents cog class
class MessageEventsCog(commands.Cog):
    '''
    A cog that handles message-related events.
    '''
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Cog event: Called when the cog is ready
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Message events cog ready")

    # Cog event: Called when a message is sent
    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        Process every messages sent by users and trigger the appropriate command.
        '''
        # Avoid processing the bot's own messages
        if message.author.bot:
            return
        # Process commands in the message content
        await self.bot.process_commands(message)

# Function to set up the cog
async def setup(bot):
    await bot.add_cog(MessageEventsCog(bot))
