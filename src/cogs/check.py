import os

from discord.ext.commands import Bot, Context


def is_not_bot(ctx: Context) -> bool:
    test_server_id = os.getenv("TEST_SERVER_ID", "")
    if test_server_id.isdecimal() and ctx.guild.id == int(test_server_id):
        return True
    return not ctx.author.bot


def setup(bot: Bot) -> None:
    checks = [is_not_bot]
    for check in checks:
        bot.add_check(check)
