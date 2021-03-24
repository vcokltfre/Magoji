from discord.ext import commands
from discord import Member


class RoleHierarchyError(commands.CheckFailure):
    def __init__(self, invoker: Member, target: Member):
        self.invoker = invoker
        self.target = target

    def __str__(self) -> str:
        return (
            f"{self.invoker.display_name}'s top role ({self.invoker.top_role}) "
            f"isn't higher than {self.target.display_name}'s top role ({self.target.top_role})."
        )
