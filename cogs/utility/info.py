import discord
from discord.ext import commands

from datetime import datetime
import textwrap


class AllInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='guild', aliases=['server'])
    async def _guild(self, ctx):
        """Sends information on the guild the command was invoked in."""

        # TODO: Add docstring

        guild = ctx.guild
        owner = guild.owner
        created = guild.created_at.strftime(
            f"%A, %B %-d, %Y at %-I:%M {'A' if ctx.guild.created_at.hour == 0 else 'P'}M UTC")
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

        embed = discord.Embed(title=f"{guild.name.title()}'s Info", timestamp=datetime.utcnow(), colour=0x87ceeb)

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


def setup(bot):
    bot.add_cog(AllInfo(bot))
