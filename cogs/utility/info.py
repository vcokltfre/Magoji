import discord
from discord.ext import commands

from datetime import datetime
import textwrap
from typing import Union

from utilities.helpers import EmbedHelper, convert_date


class AllInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='guild', aliases=['server'])
    @commands.guild_only()
    async def _guild(self, ctx: commands.Context):
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
    async def _user(self, ctx: commands.Context, user: Union[discord.Member, discord.User] = None):
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
                            **Created At:** {created}
                        """),

                            thumbnail_url=user.avatar_url,
                            fields=[{"name": "**Member Info**", "value": value}])

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AllInfo(bot))
