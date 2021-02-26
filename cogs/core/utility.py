from discord.ext import commands
from discord import Embed
from os import getenv, getpid
from git import Repo
import psutil

from internal.bot import Bot


class Core(commands.Cog):
    """A set of core commands for Magoji."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def format_bytes(size):
        power = 2 ** 10
        n = 0
        power_labels = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
        while size > power:
            size /= power
            n += 1
        return f"{round(size, 3)}{power_labels[n]+'B'}"

    @staticmethod
    def get_emoji(upper: float, value: float, above: str, below: str):
        return above if value > upper else below

    @commands.command(name="info")
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.channel)
    async def info(self, ctx: commands.Context):
        """Get info about Magoji."""
        desc = f"✅ Bot\n"
        desc += f"{self.get_emoji(0.150, self.bot.latency, ':x:', '✅')} Gateway ({round(self.bot.latency * 1000)}ms)\n\n"
        desc += f"Guilds: {len(self.bot.guilds)}"
        embed = Embed(title="Magoji Status", colour=0x87CEEB, description=desc)

        await ctx.reply(embed=embed)

    @commands.command(name="debug")
    @commands.is_owner()
    async def debug(self, ctx: commands.Context):
        """Get debug info about Magoji."""

        env = getenv("ENV", "dev")
        repo = Repo(".")
        commit = str(repo.head.commit)[:7]
        process = psutil.Process(getpid())

        mem = self.format_bytes(process.memory_info().rss)

        desc = f"Environment: {env}\nCommit: {commit}\nPID: {getpid()}\nMemory: {mem}"

        embed = Embed(title="Magoji Debug", colour=0x87CEEB, description=desc)

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx: commands.Context):
        """Make sure that bot owners are always exempt from cooldowns."""
        if await self.bot.is_owner(ctx.author):
            ctx.command.reset_cooldown(ctx)

    @commands.Cog.listener()
    async def on_ready(self):
        """Log READY events."""
        self.bot.logger.info("Bot is ready.")


class Help(commands.Cog):
    """Give help for this bot's commands."""

    def __init__(self, bot):
        bot.help_command.cog = self


def setup(bot: Bot):
    bot.add_cog(Core(bot))
    bot.add_cog(Help(bot))
