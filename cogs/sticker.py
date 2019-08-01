from discord.ext import commands


class Sticker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["emoji", "sticker"])
    async def getCustomEmojiId(self, ctx, emoji: commands.EmojiConverter):
        await ctx.send(emoji.__repr__())


def setup(bot):
    bot.add_cog(Sticker(bot))
