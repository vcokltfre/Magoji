from discord.ext import commands
from discord import Message, DMChannel
from re import compile, ASCII

from bot import Bot
from utilities.gist import create

TOKEN_RE = compile(r"([\w\-=]+)\.([\w\-=]+)\.([\w\-=]+)", ASCII)


class Core(commands.Cog):
    """Token scanning and resetting for Magoji."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """Listen for tokens and reset them by uploading to a gist."""

        await self.scan(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        """Listen for tokens and reset them by uploading to a gist."""

        await self.scan(after)

    async def scan(self, message: Message):
        """Scans a message for Discord tokens, if one is found uses Github Gist to reset it."""
        if isinstance(message.channel, DMChannel):
            return

        result = TOKEN_RE.search(message.content)
        if not result:
            return

        await message.delete()
        await message.channel.send(f"Oh no {message.author.mention}! It looks like you posted your bot token in chat, so I'm resetting it.")
        token = result.group()

        text = f"## Your token was found in a message in {message.guild}:\n{message.content}\n\n\nToken found: {token}"

        result = await create(self.bot.http_session, "tokenleak.md", "Your token was found in a message.", text)
        print(result)


def setup(bot: Bot):
    bot.add_cog(Core(bot))
