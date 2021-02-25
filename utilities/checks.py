from discord.ext.commands import check, Context
from json import loads

def command_enabled(command: str):
    async def predicate(ctx: Context):
        if not ctx.guild:
            return True

        config = await ctx.bot.db.fetch_guild(ctx.guild.id)

        if not config:
            return True

        config = loads(config[2]).get("disabled_commands", {})

        if not config:
            return True

        return command not in config

    return check(predicate)
