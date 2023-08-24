from discord.ext import commands
import discord

DEFAULT_COLOR =  0x34495E
ERROR_COLOR = 0x5865F2

def embed_error(desc: str=None):
    """Embed an error message and an optional description, footer, and url"""
    embed = discord.Embed(title="Oops!", description=desc, color=ERROR_COLOR,)
    return (embed)
