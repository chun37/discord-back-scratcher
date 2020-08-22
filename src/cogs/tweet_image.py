import re
from typing import Any, Callable, List

import aiohttp
import bs4
from bs4 import BeautifulSoup as bs
from discord import Message
from discord.ext.commands import Bot, Cog

TWEET_URL_PATTERN = re.compile(r"https?://twitter.com/\S+/status/\d+")


class TweetImage(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def get_tweet_imageurls(self, url: str) -> List[str]:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Discordbot/2.0; +https://discordapp.com/)"
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as res:
                data = await res.text()
        tags = bs(data, "lxml").select("meta[property=og\\:image]")
        get_url: Callable[[bs4.element.Tag], Any] = lambda x: x["content"]
        return list(map(get_url, tags))

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if TWEET_URL_PATTERN.search(message.content) is None:
            return
        for url in TWEET_URL_PATTERN.findall(message.content):
            urls = await self.get_tweet_imageurls(url)
            if len(urls) <= 1:
                return
            await message.channel.send("2枚目以降の画像:\n" + "\n".join(urls[1:]))
        return


def setup(bot: Bot) -> None:
    bot.add_cog(TweetImage(bot))
