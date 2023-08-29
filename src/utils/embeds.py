from discord.ext import commands
import discord

DEFAULT_COLOR =  0x5865F2
HELP_COLOR = 0x9C84EF
WARNING_COLOR = 0xfb8500
ERROR_COLOR = 0xef233c
SUCCESS_COLOR = 0x70e000

def error_embed(title : str="Oops!", desc: str=None):
    '''
    Embed an error message and an optional description, footer, and url
    '''
    embed = discord.Embed(title=title, description=desc, color=ERROR_COLOR)
    return (embed)

def warning_embed(title : str="Warning!", desc: str=None):
    '''
    Embed a warning message and an optional description, footer, and url
    '''
    embed = discord.Embed(title=title, description=desc, color=WARNING_COLOR)
    return (embed)

def success_embed(title: str="Success!", desc: str=None):
    '''
    Embed a sucess message and an optional description, footer, and url
    '''
    embed = discord.Embed(title=title, description=desc, color=SUCCESS_COLOR)
    return (embed)

def default_embed(title: str=None, desc: str=None):
    '''
    An embed with default color
    '''
    embed = discord.Embed(title=title, description=desc, color=DEFAULT_COLOR)
    return (embed)