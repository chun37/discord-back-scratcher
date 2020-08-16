from discord.ext import commands


class RestartSignal(Exception):
    pass


class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """再起動"""
        await ctx.send("再起動します")
        self.bot.exit_signal = RestartSignal()
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Restart(bot))
