import discord
from discord.ext import commands

# Define a sample module
class HelloCog(commands.Cog, name="Hello"):
    '''
    A module that contains a simple hello command for the bot.
    '''
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Cog event: Called when the cog is ready
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Hello Module ready")

    # Command definition: Hello command
    @commands.command(name="hello", description="A friendly greeting command.")
    async def hello(self, ctx: commands.Context):
        '''
        A friendly greeting command.
        '''
        await ctx.send(f"Hello, {ctx.author.mention}!")

    # others module commands...

# Function to set up the cog
async def setup(bot):
    await bot.add_cog(HelloCog(bot))
