from discord.ext import commands
from typing import Optional

from internal.bot import Bot


class Config(commands.Cog):
    """Bot configuration commands for Magoji."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="prefix")
    @commands.check_any(commands.has_permissions(manage_guild=True), commands.is_owner())
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.guild)
    async def prefix(self, ctx: commands.Context, *, p: Optional[str]):
        """Change Magoji's perfix per guild"""
        if not p:
            return await ctx.send_help(ctx.invoked_with)

        if len(p) >= 255:
            return await ctx.send("That's an invalid prefix!")

        await self.bot.db.update_guild_prefix(ctx.guild.id, p)
        await ctx.send(f"Your prefix for this guild has been set to: `{p}`")


def setup(bot: Bot):
    bot.add_cog(Config(bot))
