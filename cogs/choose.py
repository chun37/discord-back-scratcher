import random
from typing import Tuple

from discord.ext.commands import Bot, Context, command

from custom import CustomCog


class Choose(CustomCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(aliases=["random"])
    async def choose_one_from(self, ctx: Context, *options: Tuple[str]) -> None:
        """複数の選択肢の中から1つ選びます"""
        result = random.choice(options)
        await ctx.send(result)


def setup(bot: Bot) -> None:
    bot.add_cog(Choose(bot))
