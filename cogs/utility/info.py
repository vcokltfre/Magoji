import discord
from discord.ext import commands

from datetime import datetime
import textwrap
from typing import Union, Tuple
from types import ModuleType
from inspect import getsourcelines, getsourcefile
from pathlib import Path

GITHUB_REPO_URL = "https://github.com/vcokltfre/Magoji"

class SourceConverter(commands.Converter):
    """A Converter that converts a string to a Command, Cog or Extension."""
    async def convert(self, ctx: commands.Context, argument: str) -> Union[commands.Command, commands.Cog, ModuleType]:
        if command := ctx.bot.get_command(argument):
            return command
        
        if cog := ctx.bot.get_command(argument):
            return cog

        if extension := ctx.bot.extensions.get(argument):
            return extension
        raise commands.BadArgument('Not a valid Command, Cog nor Extension.')

class AllInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def convert_date(self, date: datetime):
        """Converts a datetime object to a formatted string."""

        return date.strftime(
            f"%A, %B %-d, %Y at %-I:%M {('A', 'P')[date == 0]}M UTC")

    @commands.command(name='guild', aliases=['server'])
    async def _guild(self, ctx):
        """Sends information on the guild the command was invoked in."""
        guild = ctx.guild
        owner = guild.owner
        created = self.convert_date(guild.created_at)

        num_roles = len(guild.roles)
        emojis = len(guild.emojis)
        members = guild.members

        presences = {'online': 0,
                     'offline': 0,
                     'idle': 0,
                     'dnd': 0}

        member_type = {'user': 0,
                       'bot': 0}

        for member in guild.members:
            presences[str(member.status)] += 1
            member_type[('user', 'bot')[member.bot]] += 1

        online, offline, idle, dnd = presences.values()
        users, bots = member_type.values()

        embed = discord.Embed(title=f"{guild.name.title()}'s Info",
                              timestamp=datetime.utcnow(),
                              colour=0x87ceeb)

        embed.description = textwrap.dedent(f"""
            **Owner:** {owner.mention}
            **Created At:** {created}
            **Emojis:** {emojis}
            **Roles:** {num_roles}
        """)

        embed.add_field(name=f"**Total Member Count:** {len(members)}", value=textwrap.dedent(f"""
            Users: {users}
            Bots: {bots}
            Online: {online}
            Offline: {offline}
            Idle: {idle}
            Dnd: {dnd}
        """))

        embed.add_field(name=f"**Total Channel Count:** {len(guild.channels)}",
                        value='\n'.join(f"{category.name}: {len(category.channels)}" for category in guild.categories))

        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"Command Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name='user', aliases=['member'])
    async def _user(self, ctx, user: Union[discord.Member, discord.User] = None):
        """Sends info related to the user."""

        # TODO: Add comments

        user = user or ctx.author

        created = self.convert_date(user.created_at)
        joined = self.convert_date(user.joined_at)

        roles = user.roles[1:]

        embed = discord.Embed(title=f"{str(user).title()}'s Info",
                              colour=0x87ceeb)

        embed.description = textwrap.dedent(f"""
                    **User:** {user.mention}
                    **ID:** {user.id}
                    **Created At:** {created}
                """)

        embed.add_field(name="**Member Info**", value=textwrap.dedent(f"""
                    Joined At: {joined}
                    Roles: {', '.join(r.mention for r in reversed(roles))}
                """))

        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.group(aliases=('src',), invoke_without_command=True)
    async def source(self, ctx: commands.Context, *, source_item: SourceConverter=None):
        await self.github(ctx, source_item=source_item)
    
    @source.command()
    async def github(self, ctx: commands.Context, *, source_item: SourceConverter=None):
        if source_item is None:
            embed = discord.Embed(title="Magoji's Github Repository", description=f"[Here's the github link!]({GITHUB_REPO_URL})")
            return await ctx.send(embed=embed)
        embed = self.build_embed(source_item)
        await ctx.send(embed=embed)
        
    def get_github_url(self, source_item):    
        if isinstance(source_item, commands.Command):
            src = source_item.callback.__code__
            filename = src.co_filename
        elif isinstance(source_item, ModuleType):
            src = source_item
            filename = src.__file__
        else:
            src = type(source_item)
            filename = getsourcefile(src)

        lines, first_line_no = self.get_source_code(source_item)
        if first_line_no:
            lines_extension = f"#L{first_line_no}-L{first_line_no+len(lines)-1}"
        lines_extension = lines_extension or ""
            
        file_location = Path(filename).relative_to(Path.cwd()).as_posix()

        url = f"{GITHUB_REPO_URL}/blob/master/{file_location}{lines_extension}"

        return url, file_location, first_line_no or None

    @source.command()
    async def code(self, ctx: commands.Context, *, source_item: SourceConverter):
        source = self.get_source_code(source_item)[1]
        source_name = getattr(source_item, 'name', False) or getattr(source_item, '__name__')
        escaped = source.replace('```', '`\u200b' * 3)
        embed = discord.Embed(title=f'Source Code for `{source_name}`',
                              description=f"```py\n{escaped}```",
                              colour=0x87CEEB)
        await ctx.send(embed=embed)

    def get_source_code(self, source_item: Union[commands.Command, commands.Cog, ModuleType]) -> Tuple[str, int]:
        if isinstance(source_item, (commands.Cog, ModuleType)):
            source = getsourcelines(source_item)[0]
        elif isinstance(source_item, commands.Command):
            source = getsourcelines(source_item.callback)

        return source

    def build_embed(self, source_object):
        """Build embed based on source object."""
        url, location, first_line = self.get_github_url(source_object)

        if isinstance(source_object, commands.HelpCommand):
            title = "Help Command"
            description = source_object.__doc__.splitlines()[1]
        elif isinstance(source_object, commands.Command):
            description = source_object.short_doc
            title = f"Command: {source_object.qualified_name}"
        elif isinstance(source_object, ModuleType):
            title = f"Extension: {source_object.__name__}"
        else:
            title = f"Cog: {source_object.qualified_name}"
            description = source_object.description.splitlines()[0]

        embed = discord.Embed(title=title, description=description, colour = 0x87CEEB)
        embed.add_field(name="Source Code", value=f"[Here's the Github link!]({url})")
        line_text = f":{first_line}" if first_line else ""
        embed.set_footer(text=f"{location}{line_text}")

        return embed
        

def setup(bot):
    bot.add_cog(AllInfo(bot))
