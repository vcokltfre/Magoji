from os import getenv

from internal.bot import Bot

bot = Bot()

bot.load_extension("jishaku")
bot.load_extensions(
    "core.utility",
    "core.config",
    "utility.info",
    "utility.tokens"
    "moderation.moderation",
    "moderation.logging",
)

bot.run(getenv("TOKEN"))
