from discord import Embed
from discord.ext import commands

from utils import fetch_async


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["search"])
    async def search_local_music(self, ctx, text):
        if text.isdecimal():
            query = f"select * from local_music where id == {text}"
            fetch = "one"
        else:
            query = f"select * from local_music where title like '%{text}%'"
            fetch = "all"
        response = await fetch_async(fetch, query)

        def set_field(parent, item, inline):
            id_, title, artist, _ = item
            parent.add_field(
                name=f"ID: {id_}",
                value=f"""Title: **{title}**
                Artist: **{artist}**""",
                inline=inline
            )
        embed = Embed(title="Search result")
        if fetch == "one":
            set_field(embed, response, False)
        else:
            for item in response[:20]:
                set_field(embed, item, True)
            if len(response) > 20:
                embed.set_footer(text="and more…")
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Search(bot))
