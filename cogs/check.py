import os


def is_not_bot(ctx):
    if ctx.guild.id == int(os.getenv("TEST_SERVER_ID")):
        return True
    return not ctx.author.bot


def setup(bot):
    checks = [is_not_bot]
    for check in checks:
        bot.add_check(check)
