from discord.ext.commands import Bot, Context, command, is_owner

from custom import CustomCog


class Restart(CustomCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    @is_owner()
    async def restart(self, ctx: Context) -> None:
        """再起動"""
        await ctx.send("再起動します")
        await self.bot.logout()


def setup(bot: Bot) -> None:
    bot.add_cog(Restart(bot))
