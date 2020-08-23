from discord import Embed
from discord.ext.commands import Bot, Cog, Context, EmojiConverter, command


class Sticker(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="emoji", aliases=["sticker"])
    async def get_custom_emoji_id(self, ctx: Context, emoji: EmojiConverter) -> None:
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


def setup(bot: Bot) -> None:
    bot.add_cog(Sticker(bot))
