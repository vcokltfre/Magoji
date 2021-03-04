import discord
from discord.ext import commands, menus

from datetime import datetime
import textwrap
from typing import Optional
import asyncio

from utilities.helpers import EmbedHelper, CustomTimeConverter, convert_date
from internal.context import Context


class ListSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)

    async def format_page(self, menu, page):
        return page


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

        await asyncio.sleep(1.6)

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

        cid = next(self.bot.idgen)


        await ctx.send(f'Added note to member: {member} with the content:\n```{content}```\nCase ID: {cid}')


        await self.bot.db.execute('''INSERT INTO Cases(id, guildid, userid, modid, username, modname, case_type, case_data, created_at)
                                  VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)''', cid, ctx.guild.id, member.id,
                                  ctx.author.id, str(member), str(ctx.author), "note", content, datetime.now())
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def notes(self, ctx: Context, member: discord.Member):

        rows = await self.bot.db.fetch(
                '''SELECT id, guildid, userid, modid, username, modname, case_data, created_at
                FROM Cases WHERE guildid = $1 AND userid = $2''', ctx.guild.id, member.id)

        if rows:
            embeds = []
            for row in rows:
                embed = EmbedHelper(title=f"{row[4].title()}'s Notes",
                                    description=textwrap.dedent(f"""
                                    **Case ID:** {row[0]}
                                                        
                                    **Case Author:** {row[5]}
                                    **Case User:** {row[4]}
                                                        
                                    **Case Data:**\n```{row[-2]}```
                                                                """),

                                    thumbnail_url=member.avatar_url,
                                    footer_text=f"Case created at {convert_date(row[-1])}",
                                    )

                embeds.append(embed)

            pages = menus.MenuPages(source=ListSource(embeds), clear_reactions_after=True)
            await pages.start(ctx)

        else:
            await ctx.send(f"unable to find any notes on {member}")

    @commands.command(aliases=['rcase'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def dcase(self, ctx: Context, id: int):

        case = await self.bot.db.fetch('''SELECT * FROM Cases WHERE id = $1''', id)

        if case:
            await self.bot.db.execute('''DELETE FROM Cases WHERE id = $1''', id)
            await ctx.send(f"removed case: {id} from our database")

        else:
            await ctx.send(f"no case found with the ID: {id}")


def setup(bot):
    bot.add_cog(StaffCommands(bot))
