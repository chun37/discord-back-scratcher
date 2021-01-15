import json
import re
from typing import List, Tuple
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup as bs
from discord import (
    AsyncWebhookAdapter,
    Embed,
    Message,
    TextChannel,
    User,
    Webhook,
    utils,
)
from discord.errors import Forbidden, NotFound
from discord.ext.commands import Bot, Context, bot_has_permissions, command

from custom import CustomCog

AMAZON_URL_PATTERN = re.compile(r"https?://\S+?amazon\.co\.jp\S*?/dp/\S{10}\S*")
MESSAGE_LINK_PATTERN = re.compile(
    r"https?://.*?discordapp.com/channels/\d+/(\d+)/(\d+)"
)


class OwnershipError(Exception):
    pass


def escape_markdown(text: str) -> str:
    return re.sub(r"([*_`~|])", r"\\\1", text)


def generate_reply_message(
    shorten_message: str, ref: Message
) -> Tuple[str, List[Embed]]:
    content = f"{ref.author.mention}\n{shorten_message}"
    embed = Embed(description=ref.content, timestamp=ref.created_at)
    embed.set_author(name=ref.author.name, icon_url=ref.author.avatar_url)
    embed.set_footer(text=f"{ref.guild.name}, #{ref.channel.name}")
    embeds = [embed]
    return content, embeds


class AmazonShortLink(CustomCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def send_message(
        self,
        text: str,
        user: User,
        webhook_url: str,
        embeds: List[Embed],
    ) -> None:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                webhook_url, adapter=AsyncWebhookAdapter(session)
            )
            await webhook.send(
                text,
                username=user.display_name,
                avatar_url=user.avatar_url,
                embeds=embeds,
            )

    async def get_or_create_webhook(self, channel: TextChannel) -> Webhook:
        webhooks = await channel.webhooks()

        if my_webhook := utils.get(webhooks, user__id=self.bot.user.id):
            return my_webhook

        avatar_bytes = await self.bot.user.avatar_url.read()

        my_webhook = await channel.create_webhook(name="kaede-bot", avatar=avatar_bytes)

        return my_webhook

    @staticmethod
    def get_shorten_url(url: str) -> str:
        parsed_url = urlparse(url)

        dp_index = parsed_url.path.find("/dp")
        dp_path = parsed_url.path[dp_index : dp_index + 14]

        replaced_url = parsed_url._replace(path=dp_path, query="")
        shorten_url = replaced_url.geturl()

        return shorten_url

    async def create_amazon_embed(
        self, session: aiohttp.ClientSession, url: str
    ) -> Embed:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"取得Error {url}")
                return Embed()
            res = await response.text()
        soup = bs(res, "lxml")
        if title := soup.select_one("meta[name=title]"):
            title = title["content"]
            title = title[:255] + "…" if len(title) > 256 else title
        else:
            return Embed()

        if thumbnail := soup.select_one("#landingImage"):
            thumbnail = thumbnail["src"]
        elif thumbnail := soup.select_one("#imgBlkFront"):  # 本の場合
            url_dict = json.loads(thumbnail["data-a-dynamic-image"])
            thumbnail = max(url_dict.items(), key=lambda x: sum(x[1]))[0]

        descriptions = []
        if price := soup.select_one("#priceblock_ourprice"):
            descriptions.append(price.text)
        if rating := soup.select_one('span[data-hook="rating-out-of-text"]'):
            descriptions.append(rating.text)
        if asin := url.split("/")[-1]:
            descriptions.append(f"ASIN: {asin}")

        embed = Embed(
            title=escape_markdown(title), url=url, description="\n".join(descriptions)
        )
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        return embed

    async def generate_embeds(self, urls: List[str], author_id: int) -> List[Embed]:
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
                amazon_embed = await self.create_amazon_embed(session, url)
                if amazon_embed.title is Embed.Empty:
                    continue
                embeds.append(amazon_embed)
                unique_urls.add(url)
        if not embeds:
            embeds.append(Embed())
        embeds[-1].set_footer(text=f"edited by {self.bot.user.name}, 発言者: {author_id}")
        return embeds

    @CustomCog.listener()
    async def on_message(self, message: Message) -> None:
        if message.author.bot:
            return
        if AMAZON_URL_PATTERN.search(message.content) is None:
            return

        self.on_message_bot_has_permissions(
            message.guild,
            message.channel,
            self.bot.user,
            manage_messages=True,
            manage_webhooks=True,
        )
        channel_webhook = await self.get_or_create_webhook(message.channel)

        sender = message.author
        new_message = message.content

        shorten_urls = []

        for url in AMAZON_URL_PATTERN.findall(message.content):
            shorten_url = self.get_shorten_url(url)
            new_message = new_message.replace(url, shorten_url)
            shorten_urls.append(shorten_url)
        embeds = await self.generate_embeds(shorten_urls, sender.id)

        if message.reference and isinstance(
            ref_message := message.reference.resolved, Message
        ):
            new_message, reply_embeds = generate_reply_message(new_message, ref_message)
            embeds = reply_embeds + embeds

        await message.delete()
        await self.send_message(
            new_message,
            sender,
            channel_webhook.url,
            embeds,
        )

    async def delete_message_from_channel(
        self, ctx: Context, channel: TextChannel, message_id: int
    ) -> None:  # ここ raise してるし、Optional[NoRerutn] のはずなんだけど…
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

    @command()
    @bot_has_permissions(manage_messages=True)
    async def delete(self, ctx: Context, link_or_id: str) -> None:
        """WebHookで送信したメッセージを削除します"""
        match_object = MESSAGE_LINK_PATTERN.search(link_or_id)

        if match_object:
            channel_id = int(match_object.group(1))
            message_id = int(match_object.group(2))
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except (Forbidden, NotFound):
                await ctx.send("チャンネルが取得出来ませんでした。", delete_after=30)
                return
        elif link_or_id.isdecimal():
            channel = ctx.channel
            message_id = int(link_or_id)
        else:
            await ctx.send("メッセージIDかメッセージリンクを送ってね", delete_after=30)
            return

        try:
            await self.delete_message_from_channel(ctx, channel, message_id)
        except OwnershipError as error:
            await ctx.send(*error.args, delete_after=30)


def setup(bot: Bot) -> None:
    bot.add_cog(AmazonShortLink(bot))
