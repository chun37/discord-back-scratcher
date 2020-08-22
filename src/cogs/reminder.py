import asyncio

from discord.ext import commands


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remind(self, ctx, after: int = 0, text: str = ""):
        """リマインダー(メンションします)"""
        await asyncio.sleep(after)
        await ctx.send(f"{ctx.author.mention} {text}")


def setup(bot):
    bot.add_cog(Reminder(bot))
