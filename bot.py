"""Entrypoint for running the bot."""
from os import getenv
from dotenv import load_dotenv

from internal.bot import Bot

load_dotenv()


bot = Bot()

bot.load_extension("jishaku")
bot.load_extensions(
    "core.utility",
    "core.config",
    "utility.info",
    #"utility.tokens",
)

bot.run(getenv("TOKEN"))
