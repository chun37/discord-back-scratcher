from discord.ext.commands import Bot, Context, command
from discord.utils import oauth_url

from custom import CustomCog


class Invite(CustomCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    async def invite(self, ctx: Context) -> None:
        app_info = await self.bot.application_info()
        invite_url = oauth_url(app_info.id, self.bot.permissions)
        await ctx.send(f"{self.bot.user.name} の招待リンク\n{invite_url}")


def setup(bot: Bot) -> None:
    bot.add_cog(Invite(bot))
