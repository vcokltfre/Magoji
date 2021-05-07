import discord
import datetime
import textwrap

from discord.utils import sleep_until
from discord.ext import commands
from datetime import datetime
from discord import Message

from internal.context import Context
from utilities.helpers import EmbedHelper, CustomTimeConverter


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_reminder(self, ctx: Context, msg: Message, time: datetime.datetime, *, content):
        await sleep_until(time)

        description = textwrap.dedent(f"""
        Your reminder from {time}({msg.jump_url}) has arrived:"
        ```
        {content}
        ```
        """)

        embed = EmbedHelper(
            title="Your reminder has arrived",
            description=description,

            timestamp=datetime.utcnow()
        )

        return await ctx.reply(embed=embed)



    @commands.command()
    async def remind(self, ctx: Context, time, *, content):

        time = CustomTimeConverter.convert(time)
        description = textwrap.dedent(f"""
                                    Your reminder will arive in {time} with the following content:
                                    ```
                                    {content}
                                    ```
                                    """)


        embed = EmbedHelper(
            title="Reminder Created",
            description=description,

            timestamp=datetime.utcnow()
        )

        msg = await ctx.send(embed=embed)

        await self.send_reminder(ctx, msg, time, content)
