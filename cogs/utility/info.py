import discord
from discord.ext import commands
from discord.utils import find

from datetime import datetime
import textwrap

from typing import Union, Tuple
from types import ModuleType
from inspect import getsourcelines, getsourcefile
from pathlib import Path

from utilities.helpers import EmbedHelper, convert_date
from internal.context import Context

GITHUB_REPO_URL = "https://github.com/vcokltfre/Magoji"

MIN_EXTENSION_LENGTH = 4

class SourceConverter(commands.Converter):
    """A Converter that converts a string to a Command, Cog or Extension."""

    async def convert(
        self, ctx: Context, argument: str
    ) -> Union[commands.Command, commands.Cog, ModuleType]:
        if command := ctx.bot.get_command(argument):
            if command.name == "help":
                return ctx.bot.help_command
            return command

        if cog := ctx.bot.get_cog(argument):
            return cog
    
        if len(argument[:-3]) < MIN_EXTENSION_LENGTH:
            raise commands.BadArgument("Not a valid Command, Cog nor Extension.")

        if (extension := find(lambda ext: ext[0].endswith(argument[:-3]), ctx.bot.extensions.items())) \
            and argument.endswith(".py"):
            return extension[1]

        raise commands.BadArgument("Not a valid Command, Cog nor Extension.")

        
class AllInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='guild', aliases=['server'])
    @commands.guild_only()
    async def _guild(self, ctx: Context):
        """Sends information on the guild the command was invoked in."""
        guild = ctx.guild
        owner = guild.owner
        created = convert_date(guild.created_at)

        num_roles = len(guild.roles)
        emojis = len(guild.emojis)
        members = guild.members

        presences = {'online': 0,
                     'offline': 0,
                     'idle': 0,
                     'dnd': 0}

        member_type = {'user': 0,
                       'staff': 0,
                       'bot': 0}

        for member in members:
            presences[str(member.status)] += 1
            member_type[('user', 'bot')[member.bot]] += 1
            if (member.guild_permissions.ban_members or
                    member.guild_permissions.kick_members or
                    member.guild_permissions.manage_messages):
                member_type['staff'] += 1

        online, offline, idle, dnd = presences.values()
        users, staff, bots = member_type.values()

        value2 = textwrap.dedent(f"""
            Online: {online}
            Offline: {offline}
            Idle: {idle}
            DnD: {dnd}
            """)

        value1 = textwrap.dedent(f"""
            Members: {len(members)}
            Users: {users}
            Staff: {staff}
            Bots: {bots}
            """)

        value3 = textwrap.dedent(f"""
                                Category Channels: {len(guild.categories)}
                                Voice Channels: {len(guild.voice_channels)}
                                Text Channels: {len(guild.text_channels)}
                                """)

        embed = EmbedHelper(title=f"{guild.name.title()}'s Info",
                            timestamp=datetime.utcnow(),
                            description=textwrap.dedent(f"""
                            **Owner:** {owner.mention}
                            **Created At:** {created}
                            **Emojis:** {emojis}
                            **Roles:** {num_roles}
                                    """),

                            thumbnail_url=guild.icon_url,

                            footer_text=f"Command Invoked by {ctx.author}",
                            footer_url=ctx.author.avatar_url,

                            fields=[
                                {"name": f"**Member Count:**", "value": value1},
                                {"name": "**Presences**", "value": value2},
                                {"name": f"**Total Channel Count:** {len(guild.channels)}", "value": value3, "inline": False}
                            ]
                            )

        await ctx.send(embed=embed)

    @commands.command(name='user', aliases=['member'])
    async def _user(self, ctx: Context, user: Union[discord.Member, discord.User] = None):
        """Sends info related to the user."""

        # TODO: Add comments

        user = user or ctx.author

        created = convert_date(user.created_at)
        joined = convert_date(user.joined_at)

        roles = user.roles[1:]

        value = textwrap.dedent(f"""
                    Joined At: {joined}
                    Roles: {', '.join(r.mention for r in reversed(roles))}
                """)

        embed = EmbedHelper(title=f"{str(user).title()}'s Info",
                            description=textwrap.dedent(f"""
                            **User:** {user.mention}
                            **ID:** {user.id}
                            **Bot:** {user.bot}
                            **Created At:** {created}
                        """),

                            thumbnail_url=user.avatar_url,
                            fields=[{"name": "**Member Info**", "value": value}])

        await ctx.send(embed=embed)

    @commands.command(aliases=("src", "github", "git"), invoke_without_command=True)
    async def source(
        self, ctx: Context, *, source_item: SourceConverter = None
    ):
        """Shows the github repo for this bot, include a command, cog, or extension to got to that file.
        
           If you want the source for an extension, it must end with `.py`."""
        if source_item is None:
            embed = discord.Embed(
                title="Magoji's Github Repository",
                description=f"[Here's the github link!]({GITHUB_REPO_URL})",
                colour=0x87CEEB,
            )
            return await ctx.send(embed=embed)
        embed = self.build_embed(source_item)
        await ctx.send(embed=embed)

    def get_github_url(self, source_item):
        if isinstance(source_item, (commands.HelpCommand, commands.Cog)):
            src = type(source_item)
            filename = getsourcefile(src)
        elif isinstance(source_item, commands.Command):
            src = source_item.callback.__code__
            filename = src.co_filename
        elif isinstance(source_item, ModuleType):
            src = source_item
            filename = src.__file__

        lines, first_line_no = self.get_source_code(source_item)
        lines_extension = ""
        if first_line_no:
            lines_extension = f"#L{first_line_no}-L{first_line_no+len(lines)-1}"

        file_location = Path(filename).relative_to(Path.cwd()).as_posix()

        url = f"{GITHUB_REPO_URL}/blob/master/{file_location}{lines_extension}"

        return url, file_location, first_line_no or None

    def get_source_code(
        self, source_item: Union[commands.Command, commands.Cog, ModuleType]
    ) -> Tuple[str, int]:
        if isinstance(source_item, ModuleType):
            source = getsourcelines(source_item)
        elif isinstance(source_item, (commands.Cog, commands.HelpCommand)):
            source = getsourcelines(type(source_item))
        elif isinstance(source_item, commands.Command):
            source = getsourcelines(source_item.callback)

        return source

    def build_embed(self, source_object):
        """Build embed based on source object."""
        url, location, first_line = self.get_github_url(source_object)

        if isinstance(source_object, commands.HelpCommand):
            title = "Help Command"
            help_cmd = self.bot.get_command("help")
            description = help_cmd.help
        elif isinstance(source_object, commands.Command):
            description = source_object.short_doc
            title = f"Command: {source_object.qualified_name}"
        elif isinstance(source_object, ModuleType):
            title = f"Extension: {source_object.__name__}.py"
            description = discord.Embed.Empty   
        else:
            title = f"Cog: {source_object.qualified_name}"
            description = source_object.description.splitlines()[0]

        embed = discord.Embed(title=title, description=description, colour=0x87CEEB)
        embed.add_field(name="Source Code", value=f"[Here's the Github link!]({url})")
        line_text = f":{first_line}" if first_line else ""
        embed.set_footer(text=f"{location}{line_text}")

        return embed


def setup(bot):
    bot.add_cog(AllInfo(bot))
