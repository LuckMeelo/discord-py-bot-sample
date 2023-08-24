import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Ping cog ready")

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.channel.send('Pong!')

async def setup(bot):
    await bot.add_cog(Ping(bot))