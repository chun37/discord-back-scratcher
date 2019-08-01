import os
import traceback
import asyncio

import dotenv
from discord.ext import commands

dotenv.load_dotenv()

INITIAL_COGS = [
    "cogs.check",
    "cogs.gacha",
    "cogs.choose",
    "cogs.end",
    'cogs.echo',
    "cogs.sticker",
    "cogs.tweet_image",
    "cogs.log_attachments",
    "cogs.voice",
    "cogs.restart",
]


class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="?")

        for cog in INITIAL_COGS:
            try:
                self.load_extension(cog)
            except:
                traceback.print_exc()

        self.exit_signal = None
        print(self._checks)

    async def on_ready(self):
        print(self.user.name)
        print(self.user.id, "\n")

    def run(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.start(*args, **kwargs))
        except:
            pass
        finally:
            loop.run_until_complete(self.close())
            pending = asyncio.Task.all_tasks()
            loop.run_until_complete(asyncio.gather(*pending))
            if self.exit_signal:
                raise self.exit_signal


def main():
    try_again = True
    while try_again:
        try:
            bot = MyBot()
            bot.run(os.getenv("DISCORD_TOKEN"))
        except Exception as e:
            if e.__class__.__name__ == "EndSignal":
                try_again = False
                break
            elif e.__class__.__name__ == "RestartSignal":
                pass
        finally:
            asyncio.set_event_loop(asyncio.new_event_loop())
    print("Program End.")


if __name__ == '__main__':
    main()
