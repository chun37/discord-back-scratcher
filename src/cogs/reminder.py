import asyncio

from discord.ext.commands import Bot, Cog, Context, command


class Reminder(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    async def remind(self, ctx: Context, after: int = 0, text: str = "") -> None:
        """リマインダー(メンションします)"""
        await asyncio.sleep(after)
        await ctx.send(f"{ctx.author.mention} {text}")


def setup(bot: Bot) -> None:
    bot.add_cog(Reminder(bot))
