from discord.ext.commands import Context as _BaseContext
import discord

import asyncio
import contextlib
import json
from typing import Generator, Optional, Sequence, Union


class Context(_BaseContext):
    """A Custom Context for extra functionality."""

    async def guild_config(self) -> dict:
        """Gets the config for the guild."""
        guild = await self.bot.db.fetch_guild(self.guild.id)

        if guild:
            return json.loads(guild["config"])
        return {}

    async def update_guild_config(self, **kwargs):
        """Updates the guild config."""
        config = await self.guild_config()
        config.update(kwargs)

        await self.bot.db.update_config(self.guild.id, json.dumps(config))

    @contextlib.asynccontextmanager
    async def reaction_menu(
        self,
        *,
        message: Optional[discord.Message] = None,
        prompt: discord.Embed,
        emojis: Sequence[Union[str, discord.Emoji]],
    ) -> Generator[discord.Reaction, None, None]:
        """Starts a reaction menu.
        Arguments ::
            All arguments are keyword-only.
            `message` -> The message object that will be edited to `prompt`. If None, a new message is sent.
            `prompt` -> Embed containing the prompt question.
            `emojis` -> Set of emojis that will be added as reactions.
        Yields ::
            discord.Reaction
        The context manager will automatically clear reactions."""
        if message:
            await message.edit(embed=prompt)
        else:
            message = await self.send(embed=prompt)

        emoji_set = (
            set()
        )  # casting to string for easier comparison in the check function.
        for emoji in emojis:
            await message.add_reaction(emoji)
            emoji_set.add(str(emoji))

        def check(
            reaction: discord.Reaction, user: Union[discord.Member, discord.User]
        ) -> bool:
            return (
                reaction.message == message
                and str(reaction) in emoji_set
                and user == self.author
            )

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=check, timeout=60
            )
            yield reaction
        finally:
            if not isinstance(
                message.channel, discord.DMChannel
            ):  # clearing reactions in DMs raises Forbidden
                await message.clear_reactions()
