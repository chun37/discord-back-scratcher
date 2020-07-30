import re
import aiohttp
from discord.ext import commands
from bs4 import BeautifulSoup as bs

TWEET_URL_PATTERN = re.compile(r"https?://twitter.com/\S+/status/\d+")


class TweetImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_tweet_imageurls(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com/)"
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as res:
                data = await res.text()
        tags = bs(data, "lxml").select("meta[property=og\\:image]")
        return list(map(lambda x: x["content"], tags))

    @commands.Cog.listener()
    async def on_message(self, message):
        if TWEET_URL_PATTERN.search(message.content) is None:
            return
        for url in TWEET_URL_PATTERN.findall(message.content):
            urls = await self.get_tweet_imageurls(url)
            if len(urls) <= 1:
                return
            await message.channel.send("2枚目以降の画像:\n" + "\n".join(urls[1:]))
        return


def setup(bot):
    bot.add_cog(TweetImage(bot))
