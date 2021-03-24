from discord.ext import commands
from discord.ext.commands import CommandError, CommandOnCooldown

from internal.context import Context
from internal.bot import Bot

from utilities.helpers import EmbedHelper


class ErrorHandler(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError) -> None:
        error = getattr(error, "original", error)

        if isinstance(error, CommandOnCooldown):
            if self.bot.is_owner(ctx.author):
                await ctx.reinvoke()
                return

        await self.send_error_message(ctx, error)

    async def send_error_message(self, ctx: Context, error: Exception) -> None:
        await ctx.send(embed=EmbedHelper.from_exception(error))


def setup(bot: Bot):
    bot.add_cog(ErrorHandler(bot))
