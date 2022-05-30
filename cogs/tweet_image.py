import os
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

import tweepy
import typedjson
from discord import Message
from discord.ext.commands import Bot

from custom import CustomCog

TWEET_URL_PATTERN = re.compile(r"https?://twitter.com/\w+/status/\d+")


def get_twitter_api() -> tweepy.API:
    auth = tweepy.OAuthHandler(
        os.environ["TWITTER_CONSUMER_KEY"], os.environ["TWITTER_CONSUMER_SECRET"]
    )
    auth.set_access_token(
        os.environ["TWITTER_ACCESS_TOKEN"], os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    )
    api = tweepy.API(auth)
    return api


@dataclass(frozen=True)
class Media:
    id: int
    id_str: str
    indices: List[int]
    media_url: str
    media_url_https: str
    url: str
    display_url: str
    expanded_url: str
    type: str


def get_serialized_media(json: Dict[str, Any]) -> Media:
    obj: Media = typedjson.decode(Media, json)
    return obj


class TweetImage(CustomCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.twitter_api = get_twitter_api()

    async def get_tweet_imageurls(self, url: str) -> List[str]:
        tweet_id = url.split("/")[-1]
        status = self.twitter_api.get_status(tweet_id)

        # 2枚以上画像があると、extended_entitiesにデータが入る
        if getattr(status, "extended_entities", None) is None:
            print(f"2つ以上の画像が無いよ {tweet_id=}")
            return []

        serialized_media = map(get_serialized_media, status.extended_entities["media"])
        get_url: Callable[[Media], str] = lambda x: x.media_url_https
        photo_filter: Callable[[Media], bool] = lambda media: media.type == "photo"
        return list(map(get_url, filter(photo_filter, serialized_media)))

    @CustomCog.listener()
    async def on_message(self, message: Message) -> None:
        if message.author.bot:
            return
        if TWEET_URL_PATTERN.search(message.content) is None:
            return
        for url in TWEET_URL_PATTERN.findall(message.content):
            urls = await self.get_tweet_imageurls(url)
            if len(urls) < 2:
                return
            await message.channel.send("2枚目以降の画像:\n" + "\n".join(urls[1:]))
        return


def setup(bot: Bot) -> None:
    bot.add_cog(TweetImage(bot))
