import discord
from discord.ext import commands

import utils.embeds as embeds


class CommandEventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Command events cog ready")

    @commands.Cog.listener()
    async def on_command_completion(self, context: commands.Context) -> None:
        '''
        The code in this event is executed every time a normal command has been *successfully* executed.
        '''
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])

        if context.guild is not None:
            self.bot.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
        else:
            self.bot.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")

    @commands.Cog.listener()
    async def on_command_error(self, context: commands.Context, error) -> None:
        '''
        The code in this event is executed every time a normal valid command catches an error.
        '''
        if isinstance(error, commands.CommandNotFound):
            self.bot.logger.warning(
                f"Command not found: {context.message.content} by {context.author} (ID: {context.author.id})")

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


async def setup(bot):
    await bot.add_cog(CommandEventsCog(bot))


import discord
from discord.ext import commands

# Importing utility modules (assuming they contain custom functions or classes)
import utils.embeds as embeds

# Define the CommandEventsCog cog class
class CommandEventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # Cog event: Called when the cog is ready
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Command events cog ready")

    # Cog event: Called when a command is successfully executed
    @commands.Cog.listener()
    async def on_command_completion(self, context: commands.Context) -> None:
        '''
        This event is executed every time a normal command has been *successfully* executed.
        '''
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])

        if context.guild is not None:
            self.bot.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
        else:
            self.bot.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")

    # Cog event: Called when a command catches an error
    @commands.Cog.listener()
    async def on_command_error(self, context: commands.Context, error) -> None:
        '''
        This event is executed every time a normal valid command catches an error.
        '''
        # Handle different types of errors
        if isinstance(error, commands.CommandNotFound):
            self.bot.logger.warning(
                f"Command not found: {context.message.content} by {context.author} (ID: {context.author.id})")

        elif isinstance(error, commands.CommandOnCooldown):
            # Calculate the cooldown in hours, minutes, and seconds
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            
            # Create and send an error embed
            embed = embeds.embed_error(
                description=f"**Please slow down** - You can use this command again in \
                    {f'{round(hours)} hours' if round(hours) > 0 else ''} \
                        {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} \
                            {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            # Create and send an error embed for missing permissions
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

        # ... (other error cases)
        
        else:
            raise error

# Function to set up the cog
async def setup(bot):
    await bot.add_cog(CommandEventsCog(bot))
