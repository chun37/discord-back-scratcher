import sys

from discord.ext.commands import Bot, Context, command, is_owner, bot_has_permissions

from custom import CustomCog


class EndSignal(Exception):
    pass


class End(CustomCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    @is_owner()
    @bot_has_permissions(add_reactions=True)
    async def end(self, ctx: Context) -> None:
        """終了"""
        await ctx.message.add_reaction("\N{WAVING HAND SIGN}")
        await self.bot.logout()
        sys.exit()


def setup(bot: Bot) -> None:
    bot.add_cog(End(bot))
