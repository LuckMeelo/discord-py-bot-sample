import discord
from discord.ext import commands

class GeneralCog(commands.Cog, name="General"):
    '''
    A cog that contains general commands for the bot.
    '''
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Help Module ready")

    @commands.command(name="help", description="Get information about bot modules and commands.")
    async def help(self, ctx, *modules):
        '''
        Displays information about bot modules and commands.
        '''

        prefix = self.bot.config.get('prefix') # Bot's command prefix loaded from config
        version = self.bot.config.get('version') # Bot's version loaded from config
        link = self.bot.config.get('link') # Bot's link loaded from config
        owner = self.bot.config.get('owner_id') # Bot owner's Discord ID loaded from config

        # Checks if a module parameter was given
        # If not, sends all modules and commands not associated with a cog
        if not modules:
            # Checks if the owner is on this server to mention them
            try:
                owner = ctx.guild.get_member(owner).mention
            except AttributeError:
                pass

            # Build the initial embed
            emb = discord.Embed(title='Commands and Modules', color=discord.Color.blue(),
                                description=f'Use `{prefix}help <module>` to learn more about a module :smiley:\n')

            # Adding the list of cogs to the embed
            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'
            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            # Adding uncategorized commands to the embed
            commands_desc = ''
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'
            if commands_desc:
                emb.add_field(name='Not Belonging to a Module', value=commands_desc, inline=False)

            # Information about the author and bot version
            emb.add_field(name="About", value=f"This bot is developed and maintained by <@{owner}>\n\
                                    Please visit {link} to submit ideas or bugs.")
            emb.set_footer(text=f"Bot is running version {version}")

        # Block called when one module name is given
        elif len(modules) == 1:
            for cog in self.bot.cogs:
                if cog.lower() == modules[0].lower():
                    emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
                                        color=discord.Color.green())
                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    break
            else:
                emb = discord.Embed(title="Module Not Found",
                                    description=f"I haven't heard of a module called `{modules[0]}` before :scream:",
                                    color=discord.Color.orange())

        # Too many module names requested - only one at a time allowed
        elif len(modules) > 1:
            emb = discord.Embed(title="Too Many Modules",
                                description="Please request only one module at a time :sweat_smile:",
                                color=discord.Color.orange())

        else:
            emb = discord.Embed(title="Magical Place",
                                description="I don't know how you got here, but I didn't expect this.\n"
                                            "Please report this issue on GitHub: "
                                            "https://github.com/nonchris/discord-fury/issues\n"
                                            "Thank you! ~Chris",
                                color=discord.Color.red())

        # Send the reply embed
        await ctx.send(embed=emb)

async def setup(bot):
    await bot.add_cog(GeneralCog(bot))