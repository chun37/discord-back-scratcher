import asyncio
import os
import sys
import traceback

import dotenv
from discord.ext.commands import Bot, when_mentioned_or, BotMissingPermissions

from utils import permissions_to_error_text


dotenv.load_dotenv()

INITIAL_COGS = [
    "cogs.amazon_link",
    "cogs.check",
    "cogs.choose",
    "cogs.echo",
    "cogs.end",
    "cogs.restart",
    "cogs.sticker",
    "cogs.tweet_image",
    "cogs.unquote_link",
    "cogs.reminder",
]


class MyBot(Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=when_mentioned_or("?"))
        for cog in INITIAL_COGS:
            try:
                self.load_extension(cog)
            except:
                traceback.print_exc()

    async def on_ready(self) -> None:
        print(self.user.name)
        print(self.user.id, "\n")

    def run(self, token: str) -> None:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.start(token))
        except KeyboardInterrupt:
            print("Program End.")
            sys.exit()
        finally:
            loop.run_until_complete(self.close())

    async def on_error(self, *args, **kwargs):
        error_type, error, _traceback = sys.exc_info()
        if isinstance(error, BotMissingPermissions):
            _, message, *_ = args
            await message.channel.send(permissions_to_error_text(error.missing_perms))
        else:
            traceback.print_exception(error_type, error, _traceback)

def main() -> None:
    while True:
        bot = MyBot()
        bot.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
