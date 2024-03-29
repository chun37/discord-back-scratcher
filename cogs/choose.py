import random
from typing import Sequence

from discord.ext.commands import Bot, Context, command

from custom import CustomCog


class Choose(CustomCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(aliases=["random"])
    async def choose_one_from(self, ctx: Context, *options: str) -> None:
        """複数の選択肢の中から1つ選びます"""
        await self._choose_one_from(ctx, options)

    @staticmethod
    async def _choose_one_from(ctx: Context, options: Sequence[str]) -> None:
        result = random.choice(options)
        await ctx.send(result)


def setup(bot: Bot) -> None:
    bot.add_cog(Choose(bot))
