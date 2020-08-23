import asyncio
import os
import traceback

import dotenv
from discord.ext import commands

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


class MyBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or("?"))

        for cog in INITIAL_COGS:
            try:
                self.load_extension(cog)
            except:
                traceback.print_exc()

        self.exit_signal = None

    async def on_ready(self) -> None:
        print(self.user.name)
        print(self.user.id, "\n")

    def run(self, token: str) -> None:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.start(token))
        except:
            pass
        finally:
            loop.run_until_complete(self.close())
            if self.exit_signal:
                raise self.exit_signal


def main() -> None:
    try_again = True
    while try_again:
        try:
            bot = MyBot()
            bot.run(os.environ["DISCORD_TOKEN"])
        except Exception as error:
            if error.__class__.__name__ == "EndSignal":
                try_again = False
                break
        finally:
            asyncio.set_event_loop(asyncio.new_event_loop())
    print("Program End.")


if __name__ == "__main__":
    main()
