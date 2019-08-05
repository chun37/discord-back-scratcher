import os

from discord.ext import commands

LOG_DIR = os.getenv("LOG_DIR")


class LogAttachments(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if bool(message.attachments) is False:
            return
        for attachment in message.attachments:
            guild_dir = LOG_DIR + str(message.guild.id)
            filename = "-".join(attachment.url.split("/")[-2:])
            file_type = "files" if attachment.width is None else "images"
            full_path = guild_dir + "/" + file_type

            if not os.path.exists(full_path):
                os.makedirs(full_path)

            with open(full_path + "/" + filename, "wb") as f:
                await attachment.save(f)
        return


def setup(bot):
    bot.add_cog(LogAttachments(bot))
