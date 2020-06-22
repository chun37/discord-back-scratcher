from discord import Embed
from discord.ext import commands


class Sticker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["emoji", "sticker"])
    async def getCustomEmojiId(self, ctx, emoji: commands.EmojiConverter):
        """カスタム絵文字の情報を返します"""
        embed = Embed(title=emoji.name, url=str(emoji.url))
        embed.set_thumbnail(url=str(emoji.url))
        embed.add_field(
            name="created_at",
            value=emoji.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            inline=False,
        )
        embed.add_field(name="emoji_id", value=str(emoji.id), inline=False)
        embed.add_field(name="guild_name", value=emoji.guild, inline=False)
        embed.add_field(name="guild_id", value=str(emoji.guild_id), inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Sticker(bot))
