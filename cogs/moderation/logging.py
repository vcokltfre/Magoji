import discord
from discord.ext import commands

from internal.bot import Bot
from internal.context import Context


class Logging(commands.Cog):
    """A Cog for logging message deletes, edits, cases and more!"""
    
    def __init__(self, bot: Bot):
        self.bot = bot

def setup(bot: Bot):
    bot.add_cog(Logging(bot))