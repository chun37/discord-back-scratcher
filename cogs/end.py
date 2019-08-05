from discord.ext import commands
import exceptions


class End(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def end(self, ctx):
        await ctx.message.add_reaction('\N{WAVING HAND SIGN}')
        voice_client = ctx.guild.voice_client
        if bool(voice_client):
            await voice_client.disconnect()
        self.bot.exit_signal = exceptions.EndSignal()
        await self.bot.logout()


def setup(bot):
    bot.add_cog(End(bot))
