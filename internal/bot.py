from discord.ext import commands
from discord import Intents, Message
from aiohttp import ClientSession
from typing import Optional
from dotenv import load_dotenv
from os import getenv
from logging import getLogger, INFO
from traceback import format_exc

from utilities.database import Database
from utilities.help import Help

from .context import Context

load_dotenv()


class Bot(commands.Bot):
    """A subclass of `commands.Bot` with additional features."""

    def __init__(self, *args, **kwargs):
        self.logger = getLogger("magoji")
        self.logger.setLevel(INFO)

        intents = Intents.all()

        super().__init__(
            command_prefix=self.get_prefix,
            intents=intents,
            help_command=Help(),
            *args,
            **kwargs,
        )

        self.http_session: Optional[ClientSession] = None
        self.db = Database()

    def load_extensions(self, *exts):
        """Load a set of extensions, autoprefixed by 'cogs.'"""
        for ext in exts:
            try:
                self.load_extension(f"cogs.{ext}")
                self.logger.info(f"Loaded cog cogs.{ext}")
            except Exception as e:
                self.logger.error(f"Failed to load cog: cogs.{ext}: {format_exc()}")

    async def login(self, *args, **kwargs) -> None:
        """Create the aiohttp ClientSession before logging in."""

        self.http_session = ClientSession()
        await self.db.setup()

        await super().login(*args, **kwargs)

    async def get_prefix(self, message: Message) -> str:
        """Get a dynamic prefix for the bot."""

        if not message.guild:
            return ">"

        guild_config = await self.db.fetch_guild(message.guild.id)

        if not guild_config:
            return ">"

        return guild_config[1]

    async def get_context(self, message: Message):
        return await super().get_context(message, cls=Context)


if __name__ == "__main__":
    bot = Bot()

    bot.load_extension("jishaku")
    bot.load_extensions(
        "core.utility",
        "core.config",
        "utility.info",
        # "utility.tokens",
    )

    bot.run(getenv("TOKEN"))
