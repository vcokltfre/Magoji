import discord
from discord import Message, Guild
from discord.ext import commands

from internal.bot import Bot
from internal.context import Context

from json import loads
from textwrap import dedent
from os import getenv


class Logging(commands.Cog):
    """A Cog for logging message deletes, edits, cases and more!"""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def get_logging_channel(self, guild: Guild):

        db = self.bot.db
        db_guild = await db.fetch_guild(guild.id)

        if db_guild:
            config = loads(db_guild["config"])

        else:
            return

        if channel_id := config.get("log_channel"):
            return guild.get_channel(channel_id)

    @staticmethod
    def get_message_summary(msg: Message, max_len=100):
        if len(msg.content) <= max_len:
            return msg.content
        return f"{msg.content[:max_len//2]}\n...\n{msg.content[max_len//2:]}"

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        if not after.guild:
            return
        channel = await self.get_logging_channel(after.guild)
        if not channel:
            return

        elif before.content != after.content:
            before_content = before.content
            after_content = after.content

            link = None

            if len(before_content + after_content) > 200:
                data = {
                    "api_option": "paste",
                    "api_paste_private": "1",
                    "api_dev_key": getenv("PASTEBIN_KEY"),
                    "api_paste_name": f"{after.author}'s Message",
                    "api_paste_code": f"Before:\n{before_content}\nAfter:\n{after_content}",
                }
                async with self.bot.http_session.post(
                    "https://pastebin.com/api/api_post.php", data=data
                ) as response:
                    link = await response.text()
                before_content = self.get_message_summary(before)

                after_content = self.get_message_summary(after)
            if link:
                link = f"**Full Messages: ** {link}"
            allowed_mentions = discord.AllowedMentions.none()
            await channel.send(
                f"✏ `{after.author}` edited their message (`{after.id}`) in "
                f"{after.channel.mention}:\n"
                f"**Before:** {before_content}\n**After:** {after_content}\n"
                f"{link or ''}",
                allowed_mentions=allowed_mentions,
            )


def setup(bot: Bot):
    bot.add_cog(Logging(bot))
