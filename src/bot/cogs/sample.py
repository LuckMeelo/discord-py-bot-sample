import discord
from discord.ext import commands

# Define a sample module
class SampleCog(commands.Cog, name="SampleModule"):
    '''
    A module that contains a simple example command for the bot.
    '''
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Cog event: Called when the cog is ready
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Sample Module ready")

    # Command definition: Ping command
    @commands.command(name="ping", description="Responds with \"Pong!\" when the ping command is invoked.")
    async def ping(self, ctx: commands.Context) -> None:
        '''
        Responds with "Pong!" when the ping command is invoked.
        '''
        await ctx.send('Pong!')

    # others module commands...

# Function to set up the cog
async def setup(bot):
    await bot.add_cog(SampleCog(bot))
