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

# Function to set up the cog
async def setup(bot):
    await bot.add_cog(MessageEventsCog(bot))
