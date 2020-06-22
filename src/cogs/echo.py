from discord.ext import commands


class Echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx):
        await ctx.send(ctx.message.content[6:])


def setup(bot):
    bot.add_cog(Echo(bot))
