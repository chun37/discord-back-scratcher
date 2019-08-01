from discord.ext import commands
import random


class Choose(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["random"])
    async def chooseOneFrom(self, ctx, *options):
        result = random.choice(options)
        await ctx.send(result)


def setup(bot):
    bot.add_cog(Choose(bot))
