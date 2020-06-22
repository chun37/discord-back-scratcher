from src import exceptions

from discord.ext import commands


class End(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def end(self, ctx):
        """終了"""
        await ctx.message.add_reaction('\N{WAVING HAND SIGN}')
        voice_client = ctx.guild.voice_client
        if bool(voice_client):
            await voice_client.disconnect()
        self.bot.exit_signal = exceptions.EndSignal()
        await self.bot.logout()


def setup(bot):
    bot.add_cog(End(bot))
