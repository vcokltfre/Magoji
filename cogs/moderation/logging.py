import discord
from discord import Message, Guild
from discord.ext import commands

from internal.bot import Bot
from internal.context import Context

from typing import Optional
from json import loads
from textwrap import dedent
from os import getenv
from io import StringIO


class Logging(commands.Cog):
    """A Cog for logging message deletes, edits, cases and more!"""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def get_logging_channel(self, guild: Guild) -> Optional[discord.TextChannel]:

        db = self.bot.db
        db_guild = await db.fetch_guild(guild.id)

        if db_guild:
            config = loads(db_guild["config"])

        else:
            return

        if channel_id := config.get("log_channel"):
            return guild.get_channel(channel_id)

    @staticmethod
    def get_message_summary(msg: Message, max_len=100) -> str:
        if len(msg.content) <= max_len:
            return msg.content
        return f"{msg.content[:max_len//2]}\n...\n{msg.content[max_len//2:]}"

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message) -> None:
        if not after.guild:
            return
        channel = await self.get_logging_channel(after.guild)
        if not channel:
            return

        elif before.content != after.content:
            before_content = before.content
            after_content = after.content

            file = msg = None
            if len(before_content + after_content) > 200:
                file = discord.File(
                    StringIO(f"Before:\n{before_content}\n\nAfter:\n{after_content}"),
                    "message.txt",
                )
                msg = "**Full Message:**"

            before_content = self.get_message_summary(before)

            after_content = self.get_message_summary(after)

            allowed_mentions = discord.AllowedMentions.none()
            await channel.send(
                f"✏ `{after.author}` edited their message (`{after.id}`) in "
                f"{after.channel.mention}:\n"
                f"**Before:** {before_content}\n**After:** {after_content}\n"
                f"{msg or ''}",
                allowed_mentions=allowed_mentions,
                file=file,
            )


def setup(bot: Bot) -> None:
    bot.add_cog(Logging(bot))
