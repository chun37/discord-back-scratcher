import asyncio

from discord.ext.commands import Bot, Context, command

from custom import CustomCog


class Reminder(CustomCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    async def remind(self, ctx: Context, after: int = 0, text: str = "") -> None:
        """リマインダー(メンションします)"""
        await asyncio.sleep(after)
        await ctx.send(f"{ctx.author.mention} {text}")


def setup(bot: Bot) -> None:
    bot.add_cog(Reminder(bot))
