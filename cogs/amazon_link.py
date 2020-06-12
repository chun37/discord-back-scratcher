import re
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup as bs
from discord import AsyncWebhookAdapter, Embed, Webhook
from discord.errors import Forbidden, NotFound
from discord.ext import commands

AMAZON_URL_PATTERN = re.compile(r"https?://\S+?amazon\.co\.jp\S*?/dp/\S{10}\S*")
MESSAGE_LINK_PATTERN = re.compile(
    r"https?://.*?discordapp.com/channels/\d+/(\d+)/(\d+)"
)


class OwnershipError(Exception):
    pass


def escape_markdown(text):
    return re.sub(r'([*_])', r'\\\1', text)


class AmazonShortLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, text, username, avatar_url, webhook_url, embeds):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                webhook_url, adapter=AsyncWebhookAdapter(session)
            )
            await webhook.send(
                text, username=username, avatar_url=avatar_url, embeds=embeds,
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

    def get_shorten_url(self, url):
        parsed_url = urlparse(url)

        dp_index = parsed_url.path.find("/dp")
        dp_path = parsed_url.path[dp_index : dp_index + 14]

        replaced_url = parsed_url._replace(path=dp_path, query="")
        shorten_url = replaced_url.geturl()

        return shorten_url

    async def create_amazon_embed(self, session, url):
        async with session.get(url) as response:
            res = await response.text()
        asin = url.split("/")[-1]
        soup = bs(res, "lxml")
        title = soup.find("meta", attrs={"name": "title"})["content"]
        thumbnail = soup.find(
            "div", attrs={"class": "imgTagWrapper", "id": "imgTagWrapperId"}
        ).find("img")["src"]
        embed = Embed(title=escape_markdown(title),
                      url=url, description=f"ASIN: {asin}")
        embed.set_thumbnail(url=thumbnail)
        return embed

    async def generate_embeds(self, urls, author_id):
        headers = {
            "User-Agent": "python-requests/2.23.0",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "*/*",
            "Connection": "keep-alive",
        }
        unique_urls = set()
        embeds = []
        async with aiohttp.ClientSession(headers=headers) as session:
            for url in urls:
                if url in unique_urls:
                    continue
                embeds.append(await self.create_amazon_embed(session, url))
                unique_urls.add(url)
        embeds[-1].set_footer(text=f"edited by {self.bot.user.name}, 発言者: {author_id}")
        return embeds

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if AMAZON_URL_PATTERN.search(message.content) is None:
            return

        channel_webhook = await self.get_or_create_webhook(message.channel)

        sender = message.author
        sender_avatar_url = sender.avatar_url
        sender_name = sender.display_name
        new_message = message.content

        shorten_urls = []

        for url in AMAZON_URL_PATTERN.findall(message.content):
            shorten_url = self.get_shorten_url(url)
            new_message = new_message.replace(url, shorten_url)
            shorten_urls.append(shorten_url)
        embeds = await self.generate_embeds(shorten_urls, sender.id)

        await message.delete()
        await self.send_message(
            new_message, sender_name, sender_avatar_url, channel_webhook.url, embeds,
        )

    async def delete_message_from_channel(self, ctx, channel, message_id):
        try:
            message = await channel.fetch_message(message_id)
        except (Forbidden, NotFound):
            raise OwnershipError("指定のメッセージがありません。\nこのチャンネルのメッセージでなければ、リンクで指定してください。")
        if not message.embeds:
            raise OwnershipError(f"{self.bot.user.name}に編集されたメッセージのみ削除することが出来ます。")
        embed = message.embeds[-1]
        if not embed.footer:
            raise OwnershipError(f"{self.bot.user.name}に編集されたメッセージのみ削除することが出来ます。")
        footer_text = embed.footer.text
        if footer_text != f"edited by {self.bot.user.name}, 発言者: {ctx.author.id}":
            raise OwnershipError("他の人のメッセージを削除することは出来ません")

        await message.delete()

    @commands.command()
    async def delete(self, ctx, link_or_id):
        """WebHookで送信したメッセージを削除します"""
        match_object = MESSAGE_LINK_PATTERN.search(link_or_id)

        if match_object:
            channel_id = match_object.group(1)
            message_id = match_object.group(2)
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except (Forbidden, NotFound):
                return await ctx.send("チャンネルが取得出来ませんでした。", delete_after=30)
        elif link_or_id.isdecimal():
            channel = ctx.channel
            message_id = link_or_id
        else:
            return await ctx.send("メッセージIDかメッセージリンクを送ってね", delete_after=30)

        try:
            await self.delete_message_from_channel(ctx, channel, message_id)
        except OwnershipError as e:
            await ctx.send(*e.args, delete_after=30)


def setup(bot):
    bot.add_cog(AmazonShortLink(bot))
