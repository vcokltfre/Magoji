import discord
from discord.ext import commands

from datetime import datetime, timedelta
import textwrap
from typing import Optional

from utilities.helpers import EmbedHelper, CustomTimeConverter, convert_date
from internal.context import Context


class StaffCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx: Context, member: discord.Member, *, reason="No Reason Provided"):

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
                '''INSERT INTO Cases(id, guildid, userid, modid, username, modname, case_type, created_at, case_data)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)''', next(self.bot.idgen), ctx.guild.id, member.id,
                ctx.author.id, str(member),
                str(ctx.author), "kick", curtime, reason)

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
    async def _ban(self, ctx: Context, member: discord.Member, *, reason="No Reason Provided"):

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
                '''INSERT INTO Cases(id, guildid, userid, modid, username, modname, case_type, created_at, expires_at, case_data)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)''', next(self.bot.idgen), ctx.guild.id, member.id,
                ctx.author.id, str(member), str(ctx.author), "ban", curtime, "never", reason)

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
    async def tempban(self, ctx: Context, member: discord.Member, length: CustomTimeConverter, *,
                      reason="No Reason Provided"):

        # TODO: add comments and docstrings

        if member.top_role < ctx.author.top_role:

            curtime = datetime.now()
            expires = curtime + length
            expires = convert_date(expires)

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
                '''INSERT INTO Cases(id, guildid, userid, modid, username, modname, case_type, created_at, expires_at, case_data)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)''', next(self.bot.idgen), ctx.guild.id, member.id,
                ctx.author.id, str(member), str(ctx.author), "tempban", curtime, expires, reason)

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

    @commands.command(aliases=['purge', 'del', 'delete'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: Context, channel: Optional[discord.TextChannel], amount: int):
        channel = channel or ctx.channel

        await ctx.send(f"now purging {amount} messages...", delete_after=1.5)

        await channel.purge(limit=amount + 1)
        self.bot.dispatch("purge", author=ctx.author)

    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def _unban(self, ctx, user: discord.Object, *, reason="No Reason Provided"):
        try:
            cid = next(self.bot.idgen)

            await ctx.guild.unban(user)
            await self.bot.db.execute('''INSERT INTO Cases(id, guildid, userid, modid, modname, case_type, created_at)
                                      VALUES ($1, $2, $3, $4, $5, $6, $7)''', cid, ctx.guild.id, user.id,
                                      ctx.author.id, str(ctx.author), "unban", datetime.now())

            self.bot.dispatch("unban", case=cid, user_id=user.id, guild=ctx.guild, mod=ctx.author)

        except discord.HTTPException as e:
            await ctx.send(f'an error has occured when attempting to run `{ctx.prefix}{ctx.command}`: ```{e}```')

    @commands.command(aliases=['add_note', 'notea', 'notec'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def anote(self, ctx: Context, member: discord.Member, *, content: str):

        await ctx.send(f'Added note to member: {member} with the content:\n"{content}"')


        await self.bot.db.execute('''INSERT INTO Cases(id, guildid, userid, modid, username, modname, case_type, case_data)
                                  VALUES ($1, $2, $3, $4, $5, $6, $7, $8)''', next(self.bot.idgen), ctx.guild.id, member.id,
                                  ctx.author.id, str(member), str(ctx.author), "note", content)

        """
        TODO:
        create notes command to get a list of notes in a user
        """


def setup(bot):
    bot.add_cog(StaffCommands(bot))
