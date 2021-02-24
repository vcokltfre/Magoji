from discord.ext import commands

from bot import Bot


class Core(commands.Cog):
    """A set of core commands for Magoji."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def get_emoji(upper: float, value: float, above: str, below: str):
        return above if value > upper else below

    @commands.command(name="info")
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.channel)
    async def info(self, ctx: commands.Context):
        c = f"**__Magoji Status__**\n"
        c += f"✅ Bot\n"
        c += f"{self.get_emoji(0.150, self.bot.latency, ':x:', '✅')} Gateway ({round(self.bot.latency * 1000)}ms)"

        await ctx.reply(c)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context):
        """Make sure that bot owners are always exempt from cooldowns."""
        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        """Log READY events."""
        self.bot.logger.info("Bot is ready.")


def setup(bot: Bot):
    bot.add_cog(Core(bot))
