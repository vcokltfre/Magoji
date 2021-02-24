from discord.ext import commands
from discord import Intents, Message
from aiohttp import ClientSession
from typing import Optional
from dotenv import load_dotenv
from os import getenv

from utilities.database import Database

load_dotenv()


class Bot(commands.Bot):
    """A subclass of `commands.Bot` with additional features."""

    def __init__(self, *args, **kwargs):
        intents = Intents.default()
        intents.members = True

        super().__init__(
            command_prefix=self.get_prefix, intents=intents, *args, **kwargs
        )

        self.http_session: Optional[ClientSession] = None
        self.db = Database()

    async def login(self, *args, **kwargs) -> None:
        """Create the aiohttp ClientSession before logging in."""

        self.http_session = ClientSession()
        await self.db.setup()

        await super().login(*args, **kwargs)

    async def get_prefix(self, message: Message) -> str:
        """Get a dynamic prefix for the bot."""

        return ">"  # TODO: Add actual dynamic prefixing


if __name__ == "__main__":
    bot = Bot()

    bot.run(getenv("TOKEN"))
