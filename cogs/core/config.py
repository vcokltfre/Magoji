import discord
from discord.ext import commands

from typing import Optional

from internal.bot import Bot
from internal.context import Context

from utilities.helpers import EmbedHelper

class Config(commands.Cog):
    """Bot configuration commands for Magoji."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="prefix")
    @commands.check_any(
        commands.has_permissions(manage_guild=True), commands.is_owner()
    )
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.guild)
    async def prefix(self, ctx: Context, *, p: Optional[str]):
        """Change Magoji's perfix per guild"""
        if not p:
            return await ctx.send_help(ctx.invoked_with)

        if len(p) >= 255:
            return await ctx.send("That's an invalid prefix!")

        await self.bot.db.update_guild_prefix(ctx.guild.id, p)
        await ctx.send(f"Your prefix for this guild has been set to: `{p}`")

    @commands.command(name="log_channel", aliases=("logchannel",))
    @commands.check_any(
        commands.has_permissions(manage_guild=True), commands.is_owner()
    )
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.guild)
    async def _log_channel(self, ctx: Context, channel: discord.TextChannel):
        """Sets the logging channel for your server."""

        await ctx.update_guild_config(log_channel=channel.id)
        embed = EmbedHelper(title=f"✅ Logging channel has been set to {channel.mention}.")
        await ctx.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(Config(bot))
