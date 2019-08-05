import glob
import json
import random

from discord import Embed
from discord.ext import commands


class Gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ちゅんガチャ'])
    async def gacha(self, ctx):
        file = random.choice(glob.glob("tweets/*"))
        with open(file) as f:
            datas = json.loads(f.read())
        flag = True
        while flag:
            tweet = random.choice(datas)
            if not tweet["entities"]["user_mentions"]:
                flag = False
        embed = Embed(title=tweet["text"], color=0xff80c0)
        embed.set_author(
            name=f'{tweet["user"]["name"]} (@{tweet["user"]["screen_name"]})',
            icon_url=tweet["user"]["profile_image_url_https"])
        embed.set_footer(text=tweet["created_at"])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Gacha(bot))
