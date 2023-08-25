import discord
from discord.ext import commands

# Define a cog class
class FunCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Cog event: Called when the cog is ready
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Fun Module ready")

    # Command definition: Ping command
    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        '''
        Responds with "Pong!" when the ping command is invoked.
        '''
        await ctx.send('Pong!')

# Function to set up the cog
async def setup(bot):
    await bot.add_cog(FunCog(bot))
