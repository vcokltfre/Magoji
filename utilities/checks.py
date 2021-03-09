from discord.ext.commands import check, MissingPermissions
from functools import wraps
from discord import Member

from internal.context import Context


def command_enabled(command: str):
    async def predicate(ctx: Context):
        if not ctx.guild:
            return True

        config = await ctx.guild_config()

        if not config:
            return True

        disabled_commands = config.get("disabled_commands", {})

        if not disabled_commands:
            return True

        return command not in disabled_commands

    return check(predicate)


def role_hierarchy(*, ctx_arg: int = 1, member_arg: int = 2):
    """Check if the invoker's top role is higher than the member's top role."""

    def decorator(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            ctx = args[ctx_arg]
            member = args[member_arg] or kwargs.get("member")
            if not (isinstance(ctx, Context) and isinstance(member, Member)):
                return await func(
                    *args, **kwargs
                )  # Skip if they aren't the right types.

            if ctx.author.top_role <= member.top_role:
                raise Exception  # TODO: Make another role hierarchy Exception

            return await func(*args, **kwargs)

        return inner

    return decorator
