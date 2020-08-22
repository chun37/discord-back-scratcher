from discord.ext.commands import Bot, Cog, Context, command, is_owner


class EndSignal(Exception):
    pass


class End(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    @is_owner()
    async def end(self, ctx: Context) -> None:
        """終了"""
        await ctx.message.add_reaction("\N{WAVING HAND SIGN}")
        voice_client = ctx.guild.voice_client
        if bool(voice_client):
            await voice_client.disconnect()
        self.bot.exit_signal = EndSignal()
        await self.bot.logout()


def setup(bot: Bot) -> None:
    bot.add_cog(End(bot))
