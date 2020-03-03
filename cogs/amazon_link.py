import re
from urllib.parse import urlparse

import aiohttp
from discord import AsyncWebhookAdapter, Webhook
from discord.ext import commands

AMAZON_URL_PATTERN = re.compile(r"https?://\S+?amazon\.co\.jp/\S+?/dp/\S{10}")


class AmazonShortLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, text, username, avatar_url, webhook_url):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                webhook_url, adapter=AsyncWebhookAdapter(session)
            )
            await webhook.send(text, username=username, avatar_url=avatar_url)

    async def get_or_create_webhook(self, channel):
        webhooks = await channel.webhooks()
        my_webhook = None
        for webhook in webhooks:
            if webhook.user.id != self.bot.user.id:
                continue
            return webhook

        avatar_bytes = await self.bot.user.avatar_url.read()

        mywebhook = await channel.create_webhook(name="kaede-bot", avatar=avatar_bytes)

        return mywebhook

    async def get_shorten_url(self, url):
        parsed_url = urlparse(url)

        dp_index = parsed_url.path.find("/dp")
        dp_path = parsed_url.path[dp_index:]

        replaced_url = parsed_url._replace(path=dp_path, query="")
        shorten_url = replaced_url.geturl()

        return shorten_url

    @commands.Cog.listener()
    async def on_message(self, message):
        if AMAZON_URL_PATTERN.search(message.content) is None:
            return

        channel_webhook = await self.get_or_create_webhook(message.channel)

        sender = message.author
        sender_avatar_url = sender.avatar_url
        sender_name = sender.display_name
        new_message = message.content

        await message.delete()

        for url in AMAZON_URL_PATTERN.findall(message.content):
            shorten_url = await self.get_shorten_url(url)
            new_message = new_message.replace(url, shorten_url)
        await self.send_message(
            new_message, sender_name, sender_avatar_url, channel_webhook.url
        )


def setup(bot):
    bot.add_cog(AmazonShortLink(bot))
