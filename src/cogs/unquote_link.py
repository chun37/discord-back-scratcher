import re
import urllib.parse

from discord.ext import commands

URL_PATTERN = re.compile(r"https?://([-\w]+\.)+[-\w]+[-\w./()?%&=~]*")
AMAZON_URL_PATTERN = re.compile(r"https?://(www\.)?amazon\.co\.jp[-\w./?%&=~]*")


class UnquoteLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if URL_PATTERN.search(message.content) is None:
            return

        urls = []
        for url_match in URL_PATTERN.finditer(message.content):
            url = url_match[0]
            if AMAZON_URL_PATTERN.match(url):
                continue

            new_url = urllib.parse.unquote(url)
            if new_url != url:
                urls.append(new_url)

        if len(urls) == 0:
            return

        new_message = "もしかして：\n" + "\n".join(f"<{url}>" for url in urls)
        await message.channel.send(new_message)
        return


def setup(bot):
    bot.add_cog(UnquoteLink(bot))
