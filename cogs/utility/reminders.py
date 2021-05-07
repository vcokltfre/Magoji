import datetime
import textwrap

from discord.utils import sleep_until
from discord.ext import commands
from datetime import datetime
from discord import Message

from internal.context import Context
from utilities.helpers import EmbedHelper, CustomTimeConverter, get_str_time_mapping
from internal.bot import Bot


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_reminder(
        self,
        ctx: Context,
        msg: Message,
        original_time: str,
        time: datetime,
        *,
        content: str,
    ):

        description = textwrap.dedent(
            f"""
        Your reminder from [{get_str_time_mapping(original_time)['amount']} {get_str_time_mapping(original_time)['unit']}]({msg.jump_url}) ago has arrived:
        ```
        {content}
        ```
        """
        )

        embed = EmbedHelper(
            title="Your reminder has arrived",
            description=description,
            timestamp=datetime.utcnow(),
        )

        await sleep_until(time)
        return await ctx.reply(embed=embed)

    @commands.command()
    async def remind(self, ctx: Context, length: str, *, content: str):
        time = await CustomTimeConverter.convert(self, ctx, length) + datetime.utcnow()

        description = textwrap.dedent(
            f"""
                                    Your reminder will arrive in {get_str_time_mapping(length)['amount']} {get_str_time_mapping(length)['unit']}(s) with the following content:
                                    ```
                                    {content}
                                    ```
                                    """
        )

        embed = EmbedHelper(
            title="Reminder Created",
            description=description,
            timestamp=datetime.utcnow(),
        )

        msg = await ctx.send(embed=embed)

        await self.send_reminder(ctx, msg, length, time, content=content)


def setup(bot: Bot) -> None:
    bot.add_cog(Reminders(bot))
