from urllib.parse import urlparse

import aiohttp
from discord import AsyncWebhookAdapter, Embed, Webhook
from discord.ext import commands
from verbalexpressions import VerEx

verbal_expression = VerEx()
AMAZON_URL_PATTERN = (
    verbal_expression.start_of_line()
    .find("http")
    .maybe("s")
    .find("://")
    .maybe("www.")
    .find("amazon.co.jp")
    .anything_but(" ")
).compile()


class AmazonShortLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, text, username, avatar_url, webhook_url, embed):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                webhook_url, adapter=AsyncWebhookAdapter(session)
            )
            await webhook.send(
                text, username=username, avatar_url=avatar_url, embed=embed
            )

    async def get_or_create_webhook(self, channel):
        webhooks = await channel.webhooks()
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
        dp_path = parsed_url.path[dp_index : dp_index + 14]

        replaced_url = parsed_url._replace(path=dp_path, query="")
        shorten_url = replaced_url.geturl()

        return shorten_url

    def generate_embed(self, author_id):
        embed = Embed()
        embed.set_footer(text=f"edited by {self.bot.user.name}, 発言者: {author_id}")
        return embed

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

        for url_groups in AMAZON_URL_PATTERN.findall(message.content):
            url = "".join(url_groups)
            shorten_url = await self.get_shorten_url(url)
            new_message = new_message.replace(url, shorten_url)
        embed = self.generate_embed(sender.id)
        await self.send_message(
            new_message, sender_name, sender_avatar_url, channel_webhook.url, embed
        )


def setup(bot):
    bot.add_cog(AmazonShortLink(bot))
