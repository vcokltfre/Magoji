from discord.ext import commands
from discord import Member, User, Embed
from typing import Union, List

from internal.bot import Bot


class Cases(commands.Cog):
    """Moderation cases commands for Magoji."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    def cases_embeds(self, name: str, prefix: str, cases) -> List[Embed]:
        """Generate a chunked list of embeds of a user's cases."""

        formatted_cases = []
        for case in cases:
            case_id = case["id"]
            case_type = case["case_type"].ljust(4)
            case_date = str(case["created_at"]).split()[0]

            case_data = case["case_data"]
            case_summary = (
                (case_data[:64] + "...") if len(case_data) > 64 else case_data
            )
            formatted_cases.append(
                f"`{case_type}` `{case_date}` `{case_id}` {case_summary}"
            )

        embeds = []

        for i, chunk in enumerate(self.chunks(formatted_cases, 10)):
            desc = "\n".join(chunk)
            desc += f"\n\nUse `{prefix}case <num>` for more information about a specific case."
            embed = Embed(
                title=f"Cases for {name} | Page {i + 1}",
                colour=0x87CEEB,
                description=desc,
            )
            embeds.append(embed)

        return embeds

    @commands.command(name="cases", aliases=["infractions"])
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    @commands.guild_only()
    async def cases(self, ctx: commands.Context, member: Union[User, Member, int]):
        """Get moderation cases for a user."""
        if isinstance(member, (User, Member)):
            member = member.id

        cases = await self.bot.db.fetch_cases(member, ctx.guild.id)

        if not cases:
            return await ctx.send("No cases found for that user.")

        for embed in self.cases_embeds(ctx.author, ctx.prefix, cases):
            await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Cases(bot))
