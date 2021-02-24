from asyncpg import create_pool
from asyncio import get_event_loop
from os import getenv


class Database:
    """A database interface for the bot to connect to Postgres."""

    async def setup(self):
        self.pool = await create_pool(
            host=getenv("DB_HOST", "127.0.0.1"),
            port=getenv("DB_PORT", 5432),
            database=getenv("DB_DATABASE", "magoji"),
            user=getenv("DB_USER", "root"),
            password=getenv("DB_PASS", "password"),
        )
