import discord
from discord.ext import commands

from datetime import datetime, timedelta
import textwrap
from typing import Optional

from utilities.helpers import EmbedHelper, CustomTimeConverter
from internal.context import Context


class StaffCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx: Context, member: discord.Member, *, reason="Breaking The Rules"):

        # TODO: add comments and docstrings

        if member.top_role < ctx.author.top_role:

            description = textwrap.dedent(f"""
                                        **ID:** {member.id}
                                        **Bot:** {member.bot}
                                        **Reason:** {reason.title()}
                                            """)

            curtime = datetime.now()

            embed = EmbedHelper(
                title=f"Kicking {member}",
                description=description,

                footer_text=f"Kicked by {ctx.author}",
                footer_url=ctx.author.avatar_url,

                timestamp=curtime,
                thumbnail_url=member.avatar_url,
            )

            await ctx.send(embed=embed)

            await self.bot.db.execute(
                '''INSERT INTO Cases(id, guildid, userid, modid, username, modname, case_type, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)''', next(self.bot.idgen), ctx.guild.id, member.id, ctx.author.id, member,
                ctx.author, "kick", curtime)

            await member.kick(reason=reason)

        else:

            embed = EmbedHelper(title=f'An Error Has Occurred',
                                description=f'''An error has occurred when attempting to kick {member.mention}: 
                                "cannot kick members with the same/higher role as you"'''.strip('\n'),

                                thumbnail_url=member.avatar_url,

                                timestamp=datetime.now(),
                                colour=discord.Colour.red(),

                                footer_text=f"Command Attempted by {ctx.author}",
                                footer_url=ctx.author.avatar_url,
                                )

            await ctx.send(embed=embed)

    @commands.command(name="ban", aliases=['pban'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx: Context, member: discord.Member, *, reason="Breaking The Rules"):

        # TODO: add comments and docstrings


        if member.top_role < ctx.author.top_role:

            description = textwrap.dedent(f"""
                                        **ID:** {member.id}
                                        **Bot:** {member.bot}
                                        **Reason:** {reason.title()}
                                        **Length:** Permanent
                                        **Expires:** Never
                                            """)

            curtime = datetime.now()


            embed = EmbedHelper(
                title=f"Banning {member}",
                description=description,

                footer_text=f"Banned by {ctx.author}",
                footer_url=ctx.author.avatar_url,

                timestamp=curtime,
                thumbnail_url=member.avatar_url,
            )

            await ctx.send(embed=embed)

            await self.bot.db.execute(
                '''INSERT INTO Cases(id, guildid, userid, modid, username, modname, case_type, created_at, expires_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)''', next(self.bot.idgen), ctx.guild.id, member.id, ctx.author.id, member, ctx.author, "ban", curtime, "never")

            await member.ban(reason=reason)

        else:

            embed = EmbedHelper(title=f'An Error Has Occurred',
                                description=f'''An error has occurred when attempting to ban {member.mention}: 
                                "cannot ban members with the same/higher role as you"'''.strip('\n'),

                                thumbnail_url=member.avatar_url,

                                timestamp=datetime.now(),
                                colour=discord.Colour.red(),

                                footer_text=f"Command Attempted by {ctx.author}",
                                footer_url=ctx.author.avatar_url,
                                )

            await ctx.send(embed=embed)


    @commands.command(aliases=['tban'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx: Context, member: discord.Member, length : CustomTimeConverter, *, reason="Breaking The Rules"):

        # TODO: add comments and docstrings


        if member.top_role < ctx.author.top_role:

            curtime = datetime.now()
            expires = curtime + timedelta(seconds=length)

            description = textwrap.dedent(f"""
                                        **ID:** {member.id}
                                        **Bot:** {member.bot}
                                        **Reason:** {reason.title()}
                                        **Length:** {length}
                                        **Expires:** {expires}
                                            """)


            embed = EmbedHelper(
                title=f"Banning {member}",
                description=description,

                footer_text=f"Banned by {ctx.author}",
                footer_url=ctx.author.avatar_url,

                timestamp=curtime,
                thumbnail_url=member.avatar_url,
            )

            await ctx.send(embed=embed)

            await self.bot.db.execute(
                '''INSERT INTO Cases(id, guildid, userid, modid, username, modname, case_type, created_at, expires_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)''', next(self.bot.idgen), ctx.guild.id, member.id, ctx.author.id, member, ctx.author, "tempban", curtime, expires)

            await member.ban(reason=reason)

        else:

            embed = EmbedHelper(title=f'An Error Has Occurred',
                                description=f'''An error has occurred when attempting to ban {member.mention}: 
                                "cannot ban members with the same/higher role as you"'''.strip('\n'),

                                thumbnail_url=member.avatar_url,

                                timestamp=datetime.now(),
                                colour=discord.Colour.red(),

                                footer_text=f"Command Attempted by {ctx.author}",
                                footer_url=ctx.author.avatar_url,
                                )

            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(StaffCommands(bot))
