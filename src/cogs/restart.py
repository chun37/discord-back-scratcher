from discord.ext.commands import Bot, Cog, Context, command, is_owner


class RestartSignal(Exception):
    pass


class Restart(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    @is_owner()
    async def restart(self, ctx: Context) -> None:
        """再起動"""
        await ctx.send("再起動します")
        self.bot.exit_signal = RestartSignal()
        await self.bot.logout()


def setup(bot: Bot) -> None:
    bot.add_cog(Restart(bot))
