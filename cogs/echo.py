from discord.ext.commands import Bot, Context, command

from custom import CustomCog


class Echo(CustomCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    async def echo(self, ctx: Context) -> None:
        await ctx.send(ctx.message.content[6:])


def setup(bot: Bot) -> None:
    bot.add_cog(Echo(bot))
